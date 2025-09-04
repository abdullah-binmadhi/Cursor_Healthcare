/**
 * Google Apps Script to sync GitHub repository to Google Drive
 * Healthcare Analytics Project - Cursor_Healthcare
 * Author: Abdullah Bin Madhi
 * Date: 2025-09-02
 */

// Configuration
const CONFIG = {
  GITHUB_OWNER: "abdullah-binmadhi",
  GITHUB_REPO: "Cursor_Healthcare",
  DRIVE_FOLDER_NAME: "Cursor_Healthcare_Backup",
  SYNC_INTERVAL_HOURS: 24 // Sync once per day
};

/**
 * Main function to sync GitHub repository to Google Drive
 */
function syncGitHubToDrive() {
  try {
    console.log("Starting GitHub to Drive sync...");
    
    // Get or create the backup folder
    const backupFolder = getOrCreateFolder(CONFIG.DRIVE_FOLDER_NAME);
    
    // Fetch repository information
    const repoInfo = fetchRepositoryInfo();
    console.log(`Repository: ${repoInfo.full_name}`);
    console.log(`Last updated: ${repoInfo.updated_at}`);
    
    // Create a timestamped folder for this sync
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const syncFolder = backupFolder.createFolder(`Sync_${timestamp}`);
    
    // Fetch and save repository contents
    fetchAndSaveRepositoryContents(syncFolder);
    
    // Save repository metadata
    saveRepositoryMetadata(syncFolder, repoInfo);
    
    console.log("GitHub to Drive sync completed successfully!");
    
    // Send notification email (optional)
    // sendNotificationEmail();
    
  } catch (error) {
    console.error("Error during sync:", error);
    // sendErrorNotification(error);
  }
}

/**
 * Get or create a folder in Google Drive
 * @param {string} folderName - Name of the folder
 * @returns {Folder} Google Drive folder
 */
function getOrCreateFolder(folderName) {
  const folders = DriveApp.getFoldersByName(folderName);
  
  if (folders.hasNext()) {
    return folders.next();
  } else {
    return DriveApp.createFolder(folderName);
  }
}

/**
 * Fetch repository information from GitHub API
 * @returns {Object} Repository information
 */
function fetchRepositoryInfo() {
  const url = `https://api.github.com/repos/${CONFIG.GITHUB_OWNER}/${CONFIG.GITHUB_REPO}`;
  const response = UrlFetchApp.fetch(url, {
    headers: {
      'Accept': 'application/vnd.github.v3+json'
    }
  });
  
  return JSON.parse(response.getContentText());
}

/**
 * Fetch and save repository contents recursively
 * @param {Folder} folder - Google Drive folder to save contents
 * @param {string} path - Path in the repository (default: root)
 */
function fetchAndSaveRepositoryContents(folder, path = "") {
  const url = `https://api.github.com/repos/${CONFIG.GITHUB_OWNER}/${CONFIG.GITHUB_REPO}/contents/${path}`;
  
  try {
    const response = UrlFetchApp.fetch(url, {
      headers: {
        'Accept': 'application/vnd.github.v3+json'
      }
    });
    
    const contents = JSON.parse(response.getContentText());
    
    for (const item of contents) {
      if (item.type === "file") {
        saveFile(item, folder);
      } else if (item.type === "dir") {
        const subFolder = folder.createFolder(item.name);
        fetchAndSaveRepositoryContents(subFolder, item.path);
      }
    }
  } catch (error) {
    console.error(`Error fetching contents for path ${path}:`, error);
  }
}

/**
 * Save a file from GitHub to Google Drive
 * @param {Object} fileItem - GitHub file item
 * @param {Folder} folder - Google Drive folder
 */
function saveFile(fileItem, folder) {
  try {
    // For text files, we can download and save directly
    if (isTextFile(fileItem.name)) {
      const response = UrlFetchApp.fetch(fileItem.download_url);
      const content = response.getContentText();
      folder.createFile(fileItem.name, content);
    } else {
      // For binary files, we need to handle differently
      const response = UrlFetchApp.fetch(fileItem.download_url);
      const blob = response.getBlob().setName(fileItem.name);
      folder.createFile(blob);
    }
    
    console.log(`Saved file: ${fileItem.path}`);
  } catch (error) {
    console.error(`Error saving file ${fileItem.path}:`, error);
  }
}

/**
 * Check if a file is a text file based on extension
 * @param {string} filename - Name of the file
 * @returns {boolean} True if text file
 */
function isTextFile(filename) {
  const textExtensions = [
    '.txt', '.md', '.json', '.js', '.html', '.css', '.py', '.sql', '.yaml', '.yml',
    '.csv', '.xml', '.log', '.cfg', '.conf', '.ini', '.sh', '.bat', '.cmd'
  ];
  
  return textExtensions.some(ext => filename.toLowerCase().endsWith(ext));
}

/**
 * Save repository metadata to a JSON file
 * @param {Folder} folder - Google Drive folder
 * @param {Object} repoInfo - Repository information
 */
function saveRepositoryMetadata(folder, repoInfo) {
  const metadata = {
    repository: repoInfo.full_name,
    description: repoInfo.description,
    last_updated: repoInfo.updated_at,
    clone_url: repoInfo.clone_url,
    size: repoInfo.size,
    language: repoInfo.language,
    stars: repoInfo.stargazers_count,
    forks: repoInfo.forks_count,
    sync_timestamp: new Date().toISOString(),
    sync_script_version: "1.0"
  };
  
  const metadataJson = JSON.stringify(metadata, null, 2);
  folder.createFile("repository_metadata.json", metadataJson);
}

/**
 * Set up automatic triggers for periodic sync
 */
function setupTriggers() {
  // Delete existing triggers
  const triggers = ScriptApp.getProjectTriggers();
  for (const trigger of triggers) {
    ScriptApp.deleteTrigger(trigger);
  }
  
  // Create new trigger for daily sync
  ScriptApp.newTrigger('syncGitHubToDrive')
    .timeBased()
    .everyHours(CONFIG.SYNC_INTERVAL_HOURS)
    .create();
  
  console.log(`Trigger set up for sync every ${CONFIG.SYNC_INTERVAL_HOURS} hours`);
}

/**
 * Manual trigger function for testing
 */
function runManualSync() {
  syncGitHubToDrive();
}

/**
 * Send notification email on successful sync (optional)
 */
function sendNotificationEmail() {
  const email = Session.getActiveUser().getEmail();
  const subject = "GitHub to Drive Sync Completed";
  const body = `
    The GitHub repository sync to Google Drive has been completed successfully.
    
    Repository: ${CONFIG.GITHUB_OWNER}/${CONFIG.GITHUB_REPO}
    Sync Time: ${new Date().toString()}
    
    The latest version of your healthcare analytics project is now backed up in Google Drive.
  `;
  
  MailApp.sendEmail(email, subject, body);
}

/**
 * Send error notification email
 * @param {Error} error - Error object
 */
function sendErrorNotification(error) {
  const email = Session.getActiveUser().getEmail();
  const subject = "GitHub to Drive Sync Error";
  const body = `
    An error occurred during the GitHub to Drive sync:
    
    Error: ${error.toString()}
    Time: ${new Date().toString()}
    
    Please check the script logs for more details.
  `;
  
  MailApp.sendEmail(email, subject, body);
}

/**
 * Test function to verify configuration
 */
function testConfiguration() {
  console.log("Testing GitHub API connection...");
  
  try {
    const repoInfo = fetchRepositoryInfo();
    console.log("✓ GitHub API connection successful");
    console.log(`Repository: ${repoInfo.full_name}`);
    console.log(`Description: ${repoInfo.description}`);
    
    const folder = getOrCreateFolder(CONFIG.DRIVE_FOLDER_NAME);
    console.log("✓ Google Drive folder access successful");
    console.log(`Folder ID: ${folder.getId()}`);
    
    console.log("Configuration test completed successfully!");
  } catch (error) {
    console.error("Configuration test failed:", error);
  }
}