#!/usr/bin/env python
"""
Offline installation script for ANARCI that uses pre-built HMM files
"""
import os
import shutil
import subprocess
import sys

def main():
    # Get the conda environment's site-packages directory
    conda_prefix = os.environ.get('CONDA_PREFIX')
    if not conda_prefix:
        print("Error: Not in a conda environment!")
        sys.exit(1)
    
    site_packages = os.path.join(conda_prefix, 'lib', f'python{sys.version_info.major}.{sys.version_info.minor}', 'site-packages')
    anarci_dir = os.path.join(site_packages, 'anarci')
    
    print(f"Installing ANARCI to: {anarci_dir}")
    
    # Create the anarci directory
    os.makedirs(anarci_dir, exist_ok=True)
    
    # Copy the Python files
    src_files = ['__init__.py', 'anarci.py', 'schemes.py']
    for file in src_files:
        src = os.path.join('lib/python/anarci', file)
        dst = os.path.join(anarci_dir, file)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied {file}")
    
    # Copy the germlines.py from the pre-built data
    if os.path.exists('dat/germlines.py'):
        shutil.copy2('dat/germlines.py', os.path.join(anarci_dir, 'germlines.py'))
        print("Copied germlines.py")
    elif os.path.exists('temp_anarci/lib/python/anarci/germlines.py'):
        shutil.copy2('temp_anarci/lib/python/anarci/germlines.py', os.path.join(anarci_dir, 'germlines.py'))
        print("Copied germlines.py from temp_anarci")
    
    # Copy the dat directory with HMMs
    dat_src = 'dat'
    dat_dst = os.path.join(anarci_dir, 'dat')
    if os.path.exists(dat_src):
        if os.path.exists(dat_dst):
            shutil.rmtree(dat_dst)
        shutil.copytree(dat_src, dat_dst)
        print("Copied HMM data files")
    
    # Copy the ANARCI executable
    bin_dir = os.path.join(conda_prefix, 'bin')
    anarci_script = os.path.join(bin_dir, 'ANARCI')
    if os.path.exists('bin/ANARCI'):
        shutil.copy2('bin/ANARCI', anarci_script)
        os.chmod(anarci_script, 0o755)
        print("Installed ANARCI executable")
    
    print("\nANARCI installation complete!")
    print("You can now use ANARCI by running: ANARCI -h")

if __name__ == '__main__':
    main() 