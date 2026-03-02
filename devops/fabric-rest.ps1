param (
    [string]$workspaceName = "DEMO-POC",
    [string]$pipelineName = "PL_EndToEnd_DEV",
    [string]$sourceRoot = "."
)

# --- Configuration ---
$notebooksDir = "$sourceRoot/notebooks"
$baseUrl = "https://api.fabric.microsoft.com/v1"

# --- Token Acquisition ---
$token = az account get-access-token --resource https://analysis.windows.net/powerbi/api --query accessToken -o tsv
if (-not $token) {
    Write-Error "Failed to acquire Fabric access token."
    exit 1
}
Write-Host "##vso[task.setvariable variable=FABRIC_TOKEN;issecret=true]$token"

$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type"  = "application/json"
}

# --- Helper Function: Get or Create Item ---
function Get-OrCreate-Item {
    param($workspaceId, $itemName, $itemType, $definition = $null)
    
    $itemsResponse = Invoke-RestMethod -Uri "$baseUrl/workspaces/$workspaceId/items" -Method Get -Headers $headers
    $item = $itemsResponse.value | Where-Object { $_.displayName.Trim() -eq $itemName.Trim() -and $_.type -eq $itemType }
    
    if (-not $item) {
        Write-Host "Creating ${itemType}: ${itemName}..."
        $payload = @{
            displayName = $itemName
            type        = $itemType
        }
        if ($null -ne $definition) { $payload["definition"] = $definition }
        
        $createResponse = Invoke-RestMethod -Uri "$baseUrl/workspaces/$workspaceId/items" -Method Post -Headers $headers -Body ($payload | ConvertTo-Json -Depth 10)
        Write-Host "Successfully created ${itemType}: ${itemName} (ID: $($createResponse.id))"
        return $createResponse
    } else {
        Write-Host "${itemType} '${itemName}' already exists (ID: $($item.id))"
        return $item
    }
}

# --- 1. Find & Validate Workspace ---
Write-Host "Validating workspace: $workspaceName"
$workspacesResponse = Invoke-RestMethod -Uri "$baseUrl/workspaces" -Method Get -Headers $headers
$workspace = $workspacesResponse.value | Where-Object { $_.displayName.Trim() -eq $workspaceName.Trim() }

if (-not $workspace) {
    Write-Error "Workspace '$workspaceName' not found."
    exit 1
}
$workspaceId = $workspace.id
Write-Host "Workspace found. ID: $workspaceId"

# --- 2. Auto-Deploy Lakehouses ---
"LH_ReferenceData", "LH_Claims", "LH_Members", "LH_Providers" | ForEach-Object {
    Get-OrCreate-Item -workspaceId $workspaceId -itemName $_ -itemType "Lakehouse"
}

# --- 3. Auto-Deploy Notebooks from Repo ---
if (Test-Path $notebooksDir) {
    Get-ChildItem -Path $notebooksDir -Filter *.ipynb | ForEach-Object {
        $nbName = $_.BaseName
        $nbPath = $_.FullName
        $contentBase64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($nbPath))
        
        # Notebook Definition Format for Fabric Public API
        $definition = @{
            parts = @(
                @{
                    path = "notebook-content.ipynb"
                    payload = $contentBase64
                    payloadType = "InlineBase64"
                }
            )
        }
        Get-OrCreate-Item -workspaceId $workspaceId -itemName $nbName -itemType "Notebook" -definition $definition
    }
}

# --- 4. Auto-Deploy Pipeline ---
$pipeline = Get-OrCreate-Item -workspaceId $workspaceId -itemName $pipelineName -itemType "DataPipeline"
$pipelineId = $pipeline.id

# --- 5. Trigger Pipeline ---
Write-Host "Triggering pipeline: $pipelineName (ID: $pipelineId)"
$runHeaders = @{}
$runUrl = "$baseUrl/workspaces/$workspaceId/items/$pipelineId/jobs/instances?jobType=Pipeline"
$runResponse = Invoke-RestMethod -Uri $runUrl -Method Post -Headers $headers -ResponseHeadersVariable runHeaders

$runId = $runResponse.id 
if (-not $runId -and $runHeaders["Location"]) {
    $runId = $runHeaders["Location"] -split "/" | Select-Object -Last 1
}

if (-not $runId) {
    Write-Error "Failed to trigger pipeline run."
    exit 1
}
Write-Host "Pipeline Run ID: $runId"

# --- 6. Monitoring Status ---
$status = "InProgress"
while ($status -eq "InProgress" -or $status -eq "NotStarted") {
    Start-Sleep -Seconds 20
    $statusResponse = Invoke-RestMethod -Uri "$baseUrl/workspaces/$workspaceId/items/$pipelineId/jobs/instances/$runId" -Method Get -Headers $headers
    $status = $statusResponse.status
    Write-Host "Current Status: $status"
}

if ($status -eq "Succeeded" -or $status -eq "Completed") {
    Write-Host "Pipeline executed successfully."
    exit 0
} else {
    Write-Error "Pipeline finished with status: $status"
    exit 1
}
