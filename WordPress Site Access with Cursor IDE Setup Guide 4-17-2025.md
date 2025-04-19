# **WordPress Site Access with Cursor IDE Setup Guide**

## **What We Accomplished:**

1. Successfully connected Cursor IDE to your Hostinger-hosted WordPress site (BailBondsBuddy.com)  
2. Configured SFTP for direct file editing with automatic uploads on save  
3. Downloaded the WordPress files to your local environment for editing  
4. Established a workflow that allows immediate updates to the live site

## **Key Connection Details:**

### **Server Information:**

* Host: 89.116.192.143  
* Port: 65002  
* Username: u777344352  
* Authentication: SSH key at /Users/michaels/.ssh/id\_rsa

### **File Paths:**

* Remote WordPress Path: `/home/u777344352/domains/bailbondsbuddy.com/public_html`  
* Local Path: `/Users/michaels/Library/Mobile Documents/com~apple~CloudDocs/GitHub/BBB-Cursor`

### **SFTP Configuration (sftp.json):**

json  
{  
    "name": "BailBondsBuddy",  
    "host": "89.116.192.143",  
    "protocol": "sftp",  
    "port": 65002,  
    "username": "u777344352",  
    "remotePath": "/home/u777344352/domains/bailbondsbuddy.com/public\_html",  
    "uploadOnSave": true,  
    "privateKeyPath": "/Users/michaels/.ssh/id\_rsa",  
    "ignore": \[  
        ".vscode",  
        ".git",  
        ".DS\_Store",  
        "node\_modules"  
    \]

}

## **Setting Up Access for Other Domains:**

1. Create a new folder for your website (e.g., `~/Desktop/AnotherSite-Cursor`)  
2. Create sftp.json with the same configuration but change the remotePath to: `/home/u777344352/domains/your-domain-name.com/public_html`  
3. Open the folder in Cursor IDE  
4. Use Command Palette (Cmd+Shift+P) and run "SFTP: Download Project"

## **Working with your WordPress Site in Cursor:**

### **Analyzing Your WordPress Installation:**

To have Cursor understand your WordPress site structure, you can use:

find . \-type f \-name "\*.php" \-o \-name "\*.js" \-o \-name "\*.css" | grep \-v node\_modules | sort \> site-structure.txt

This creates a file listing all your code files, which helps Cursor's AI understand your site structure.

### **Setting Up Live Preview:**

1. To view your site as you edit, you can use Browser Sync or simply keep a browser window open to your site  
2. For Divi-specific previews, you can use the Divi Visual Builder through your WordPress admin

### **Building Pages with Divi and Directorist:**

1. For theme files: Navigate to `/wp-content/themes/[your-theme]`  
2. For Divi templates: Look in `/wp-content/themes/Divi/includes/builder/`  
3. For Directorist files: Find them in `/wp-content/plugins/directorist/`

### **Workflow for Creating New Pages:**

1. Edit template files in Cursor IDE  
2. Save changes (they automatically upload)  
3. Refresh your browser to see changes  
4. For Divi-specific elements, you may need to use the Divi Builder interface on the WordPress admin side

### **Database Access:**

For database changes, you'll still need to use phpMyAdmin through Hostinger's control panel.

## **Troubleshooting Tips:**

* If connection fails, verify the exact path with `ls -la ~/domains/[domain-name]`  
* Check SSH key permissions with `chmod 600 ~/.ssh/id_rsa`  
* Test SSH connection directly: `ssh -p 65002 u777344352@89.116.192.143`  
* If needed, adjust file permissions on server: `chmod -R 755 /home/u777344352/domains/[domain]/public_html`

This setup gives you an efficient workflow to directly edit your WordPress sites across all 30 domains in your Hostinger account using Cursor IDE.

