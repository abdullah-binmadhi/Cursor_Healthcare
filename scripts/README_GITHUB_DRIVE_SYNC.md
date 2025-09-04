# GitHub to Google Drive Sync for Healthcare Analytics

This script automatically syncs your GitHub repository to Google Drive, creating backups of your healthcare analytics project.

## 🚀 Setup Instructions

### 1. Create Google Apps Script Project

1. Go to [Google Apps Script](https://script.google.com/)
2. Click "New Project"
3. Remove the default `myFunction()` code
4. Copy and paste the contents of `github_to_drive_sync.js` into the editor
5. Save the project with a name like "Healthcare_GitHub_Backup"

### 2. Configure the Script

Update the configuration at the top of the script if needed:

```javascript
const CONFIG = {
  GITHUB_OWNER: "abdullah-binmadhi",     // Your GitHub username
  GITHUB_REPO: "Cursor_Healthcare",      // Your repository name
  DRIVE_FOLDER_NAME: "Cursor_Healthcare_Backup", // Backup folder name in Drive
  SYNC_INTERVAL_HOURS: 24                // How often to sync (hours)
};
```

### 3. Set Up Permissions

1. Click the "Run" button (▶️) next to the `testConfiguration` function
2. Grant required permissions when prompted:
   - View and manage your spreadsheets in Google Drive
   - Send email as you
   - Connect to an external service (GitHub API)

### 4. Test the Connection

1. Run the `testConfiguration` function to verify:
   - GitHub API connection
   - Google Drive folder access
   - Script configuration

### 5. Run Manual Sync (Optional)

1. Run the `runManualSync` function to perform an immediate sync
2. Check your Google Drive for the backup folder

### 6. Set Up Automatic Sync

1. Run the `setupTriggers` function to create automatic sync triggers
2. The script will now automatically sync every 24 hours

## 📁 What Gets Synced

The script will create backups containing:
- All files and folders from your GitHub repository
- Repository metadata (description, stars, last update, etc.)
- Timestamped folders for each sync operation

## 🔧 Troubleshooting

### Common Issues:

1. **API Rate Limiting**: GitHub has rate limits for API requests. If you see errors, try again later.

2. **Permission Errors**: Make sure you've granted all required permissions when prompted.

3. **Large Files**: Very large binary files may not sync properly due to Google Apps Script limitations.

### Checking Logs:

1. In the Apps Script editor, go to "View" → "Logs"
2. Or click "Executions" in the left sidebar to see detailed execution logs

## 🛡️ Security Notes

- The script only reads from your public GitHub repository
- No sensitive information is stored in the script
- All data is stored in your Google Drive
- Email notifications only go to your account

## 🔄 Sync Frequency

By default, the script syncs once per day. You can adjust this by changing the `SYNC_INTERVAL_HOURS` value in the configuration.

## 📧 Notifications

The script can send email notifications for:
- Successful sync completion
- Errors during sync

To enable notifications, uncomment the relevant lines in the `syncGitHubToDrive` function.

## 🆘 Support

If you encounter issues:
1. Check the execution logs in Google Apps Script
2. Verify your repository is public
3. Ensure you've granted all required permissions
4. Check that the GitHub username and repository name are correct

## 📚 Healthcare Analytics Project

This sync script is designed for the Cursor Healthcare Analytics project, which includes:
- Healthcare cost estimation tools
- Physician finder with performance metrics
- Analytics dashboards with real-time data
- Multi-year healthcare metrics visualization

The backups will preserve all project files, ensuring you never lose your healthcare analytics work.