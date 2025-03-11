# **🛠 Git Troubleshooting Guide: Fixing Divergent Branch Issues**  

This guide provides solutions for **Git users encountering the "Need to specify how to reconcile divergent branches" error** when trying to pull updates from a remote repository.  

---  

## **🔍 Why Does This Happen?**  
This error occurs when:  
- Your **local branch and the remote branch have different commits**.  
- Git doesn’t know whether to **merge, rebase, or fast-forward** the changes.  
- You need to specify a **pull strategy** to resolve the divergence.  

---

## **⚡ Quick Fixes for Different Scenarios**  

### **1️⃣ Merge (Default & Recommended) – Keep Both Changes**  
✅ **Use this if you want to merge your local commits with the remote changes** (creates a merge commit).  

**Run this command:**  
```sh
git config pull.rebase false
git pull origin main
```
📝 **What happens?**  
- Your local commits stay intact.  
- Remote changes are merged into your local branch.  

📌 **Use this when:** You want a full history, including a merge commit.  

---

### **2️⃣ Rebase – Keep a Clean History**  
✅ **Use this if you want to apply your local changes on top of the remote ones (no merge commit).**  

**Run this command:**  
```sh
git config pull.rebase true
git pull --rebase origin main
```
📝 **What happens?**  
- Remote changes are applied **first**, then your local commits are **replayed** on top.  
- This creates a **linear commit history** without unnecessary merge commits.  

📌 **Use this when:** You prefer a cleaner commit history with no merge commits.  

---

### **3️⃣ Fast-Forward Only – No Merge Allowed**  
✅ **Use this if you only want to update your branch when no local changes exist.**  

**Run this command:**  
```sh
git config pull.ff only
git pull --ff-only origin main
```
📝 **What happens?**  
- Your branch is updated **only if there are no conflicts**.  
- If your local branch has diverged, **Git will stop the process** and ask you to resolve the issue manually.  

📌 **Use this when:** You want to ensure your branch is updated only if it aligns exactly with the remote branch.  

---

## **🔄 Handling Uncommitted Changes Before Pulling**  

### **Option 1: Commit Changes** (Recommended)  
If you have **local uncommitted changes**, commit them before pulling updates:  
```sh
git add .
git commit -m "Save local changes before pulling"
git pull origin main
```

---

### **Option 2: Stash Changes (Temporary Save)**  
If you **don’t want to commit yet**, stash your changes:  
```sh
git stash
git pull origin main
git stash pop  # Restore stashed changes
```

📌 **Use this when:** You want to pull changes without committing unfinished work.  

---

## **🔥 Resolving Conflicts After Pulling**
If Git shows **merge conflicts** after pulling, follow these steps:  

### **1️⃣ Identify Conflicted Files**  
Run:  
```sh
git status
```
Git will list **files with conflicts**.  

### **2️⃣ Open and Edit Conflicted Files**  
Look for `<<<<<<< HEAD` and `>>>>>>>` markers in the files.  

Example:  
```diff
<<<<<<< HEAD
This is my local change.
=======
This is the remote change.
>>>>>>> origin/main
```
✔ **Manually edit the file to keep the correct version**, then save it.  

---

### **3️⃣ Mark Conflicts as Resolved**  
Run:  
```sh
git add .
git commit -m "Resolved merge conflicts"
```

Then push your changes:  
```sh
git push origin main
```

📌 **Use this when:** You need to **manually choose which version of the code to keep**.  

---

## **💡 Best Practices to Avoid This Issue**  

🔹 **Always pull before making changes**:  
```sh
git pull origin main
```
🔹 **Use feature branches** for new changes:  
```sh
git checkout -b new-feature
```
🔹 **Regularly push your commits** to avoid large differences between local and remote:  
```sh
git push origin main
```
🔹 **Keep Git updated** to avoid compatibility issues.  

---

## **🛠 Full Summary Table**  

| Situation | Command to Use |
|-----------|---------------|
| Merge local and remote changes | `git pull origin main` |
| Keep a clean commit history | `git pull --rebase origin main` |
| Only update if no local changes | `git pull --ff-only origin main` |
| Stash changes before pulling | `git stash && git pull origin main && git stash pop` |
| Resolve merge conflicts | Edit files, then `git add . && git commit -m "Resolve conflicts"` |
| Force push after rebasing | `git push --force origin main` |

---

## **📜 Final Notes**  

- **If unsure, use `git pull origin main` to merge safely.**  
- **Avoid force-pushing unless necessary (`git push --force`).**  
- **If conflicts appear, manually edit files and commit changes.**  
- **When in doubt, make a backup of your branch before pulling.**  
