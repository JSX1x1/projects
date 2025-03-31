# Disk Addressing Tool

## Overview

The **Disk Addressing Tool** is a Python-based utility that allows users to interact with and manage disk addresses at a low level. It offers both a **Graphical User Interface (GUI)** and a **Command-Line Interface (CLI)** version, allowing flexibility based on user preferences.

### Features:
1. **CHS to LBA Conversion**: Convert Cylinder-Head-Sector (CHS) values to Logical Block Addressing (LBA) values.
2. **LBA to CHS Conversion**: Convert Logical Block Addressing (LBA) values back to Cylinder-Head-Sector (CHS) values.
3. **Sector Status Check**: Check whether a specific sector is "used" or "free" based on its address.
4. **View Data at Sector**: Admin users can view simulated data stored at a specific sector address.
5. **Disk Scanning**: Scan the entire disk to display used and free sectors. Non-admin users will get a simulation, while admins can access actual disk data.

### Versions:
- **CLI Version**: A command-line interface for users who prefer terminal-based tools.
- **GUI Version**: A graphical user interface built with PyQt6, offering an interactive and user-friendly experience.

---

## Table of Contents
1. [Installation](#installation)
2. [Prerequisites](#prerequisites)
3. [Usage](#usage)
    - [CLI Version](#cli-version)
    - [GUI Version](#gui-version)
4. [Features](#features)
    - [CLI Features](#cli-features)
    - [GUI Features](#gui-features)
5. [Admin Privileges](#admin-privileges)
6. [License](#license)
7. [Contributing](#contributing)

---

## Installation

To run the Disk Addressing Tool on your local machine, follow these steps.

### 1. Clone the repository:

```bash
git clone https://github.com/JSX1x1//project/Utils/Client/Disk Adressing Tool.git
cd DiskAddressingTool
```
**Consider creating a path before cloning the project to prevent issues**
```bash
mkdir DiskAddressingTool
cd DiskAddressingTool
```

### 2. Install dependencies:

This tool requires Python 3.x. Additionally, you will need to install the required Python libraries. Use the following command to install dependencies:

```bash
pip install -r requirements.txt
```

The required libraries include:
- `psutil` (for accessing disk information)
- `PyQt6` (for the graphical user interface)
- `qdarkstyle` (for dark mode styling in the GUI)

### 3. (Optional) Install `psutil` if not included in requirements.txt:

```bash
pip install psutil
```

---

## Prerequisites

Ensure you have the following installed:
- **Python 3.x**
- **pip** (Python package manager)
- **Administrative privileges** (for accessing certain disk details on your system)

---

## Usage

### CLI Version

The **CLI version** of the Disk Addressing Tool provides all functionality through the terminal. To use the CLI, follow these steps:

1. Open a terminal.
2. Navigate to the directory where you have cloned the repository.
3. Run the following command:

   ```bash
   python disk_adr_tool_CLI.py
   ```

4. You'll be prompted to choose one of the following options:
    - **1**: Convert CHS to LBA.
    - **2**: Convert LBA to CHS.
    - **3**: Check the status of a sector (used or free).
    - **4**: View data at a specific sector (admin only).
    - **5**: Scan the entire disk for used or free sectors.

5. Follow the on-screen prompts to interact with the tool.

### GUI Version

The **GUI version** of the Disk Addressing Tool provides a more interactive and visually intuitive interface. To use the GUI, follow these steps:

1. Install the required dependencies, if not done already:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the following command:

   ```bash
   python disk_adr_tool_GUI.py
   ```

3. The application will launch, and you can use the provided buttons and input fields to perform the following tasks:
    - Convert **CHS to LBA**.
    - Convert **LBA to CHS**.
    - Check the **status of a sector** (used or free).
    - View **data at a sector** (admin only).
    - **Scan the entire disk** for used and free sectors.

4. Admin users will have the option to view data at specific sectors and check real disk information. Non-admin users will interact with a simulated disk.

---

## Features

### CLI Features:
- **Convert CHS to LBA**: Allow conversion from Cylinder-Head-Sector to Logical Block Addressing format.
- **Convert LBA to CHS**: Convert Logical Block Addressing to Cylinder-Head-Sector.
- **Check Sector Status**: Users can check whether a sector is "used" or "free."
- **View Data at Sector**: Admin users can see data stored at specific sectors (in a simulated environment for non-admin users).
- **Scan Entire Disk**: Scan the entire disk and list used and free sectors.

### GUI Features:
- **Interactive Conversion**: Use input fields and buttons to convert between CHS and LBA.
- **Sector Status Checking**: Allows you to check if sectors are "used" or "free."
- **View Data at Sector**: Admin users can view simulated data at a sector address.
- **Disk Scanning**: Scan the entire disk or simulated disk for used/free sectors.

---

## Admin Privileges

### Admin Users:
- Admin users can access real disk information (like detecting whether the disk is an SSD or HDD).
- Admins can view **raw data** located at specific sectors.
- Admin users can perform operations that require elevated permissions (like scanning the real disk or accessing certain sectors).

### Non-Admin Users:
- Non-admin users are provided with a **simulated disk**. They will not be able to access real disk data but can still interact with the disk tool.
- **Sector status checking** and **disk scanning** will still work, but data at specific sectors cannot be viewed.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contributing

We welcome contributions to improve the Disk Addressing Tool. To contribute:

1. Fork this repository.
2. Create a new branch (e.g., `feature-xyz`).
3. Make your changes and commit them with clear messages.
4. Push your branch to your forked repository.
5. Create a pull request describing your changes.

Please ensure that your contributions follow the project’s coding standards and include tests where applicable.

---

## Example Use Cases:

### Admin User:

1. **Check Disk Type**: Launch the tool and check whether the connected disk is an **SSD** or **HDD**.
2. **Check Sector Status**: Enter CHS values to check whether a sector is free or used on the actual disk.
3. **View Sector Data**: View the raw data located at a specific sector address (if the sector is used).
4. **Scan Entire Disk**: Perform a full scan of the disk to list all sectors and their usage status.

### Non-Admin User:

1. **Check Sector Status**: Enter CHS values to check whether a sector is free or used on the simulated disk.
2. **Scan Entire Disk**: Perform a full scan of the simulated disk to list all sectors and their usage status.

---

## Troubleshooting

- **Admin Privileges**: If the application doesn’t allow you to view real disk data or access certain sectors, ensure you have **admin privileges**. For Windows, run the application as Administrator.
  
- **Missing Dependencies**: If you encounter issues with missing modules, make sure you've installed all required dependencies by running `pip install -r requirements.txt`.

- **Permissions**: On Linux and macOS, certain disk-related operations might require root permissions. Use `sudo` to run the tool with elevated privileges.