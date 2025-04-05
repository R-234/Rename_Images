import os
import magic
import streamlit as st
from PIL import Image
import PyPDF2
from io import BytesIO
import zipfile

def validate_file(file):
    """Check if file is valid image/PDF using magic numbers"""
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(file.getvalue())
    
    if file_type.startswith('image/'):
        try:
            Image.open(file)
            return True
        except:
            return False
    elif file_type == 'application/pdf':
        try:
            PyPDF2.PdfReader(file)
            return True
        except:
            return False
    return False

def rename_files(uploaded_files, start_number, output_folder="renamed_files"):
    os.makedirs(output_folder, exist_ok=True)
    renamed_files = []
    
    for i, uploaded_file in enumerate(uploaded_files, start=start_number):
        if not validate_file(uploaded_file):
            continue
            
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        new_name = f"{i}{file_ext}"
        new_path = os.path.join(output_folder, new_name)
        
        with open(new_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        renamed_files.append((uploaded_file.name, new_name))
    
    return renamed_files

def main():
    st.title("📁 File Renamer Pro")
    st.markdown("Upload images/PDFs and rename them sequentially (e.g., 1001.jpg, 1002.pdf)")
    
    # File uploader with type restrictions
    uploaded_files = st.file_uploader(
        "Upload files",
        type=["jpg", "jpeg", "png", "pdf", "bmp", "gif"],
        accept_multiple_files=True
    )
    
    # Starting number input
    start_number = st.number_input(
        "Starting number (e.g., 1001)",
        min_value=1,
        value=1001,
        step=1
    )
    
    # Custom prefix option
    custom_prefix = st.text_input("Custom prefix (optional)", "")
    
    if uploaded_files and st.button("Rename Files"):
        with st.spinner("Processing files..."):
            # Filter out invalid files first
            valid_files = [f for f in uploaded_files if validate_file(f)]
            invalid_files = [f.name for f in uploaded_files if not validate_file(f)]
            
            if invalid_files:
                st.warning(f"Skipped invalid files: {', '.join(invalid_files)}")
            
            if valid_files:
                renamed_files = rename_files(valid_files, start_number)
                
                # Apply custom prefix if specified
                if custom_prefix:
                    renamed_files = [
                        (old, f"{custom_prefix}_{new}") 
                        for old, new in renamed_files
                    ]
                
                st.success(f"✅ Successfully renamed {len(renamed_files)} files!")
                
                # Display results
                st.subheader("Renamed Files")
                st.table([{"Original": old, "New Name": new} for old, new in renamed_files])
                
                # Create ZIP
                zip_path = "renamed_files.zip"
                with zipfile.ZipFile(zip_path, "w") as zipf:
                    for _, new_name in renamed_files:
                        file_path = os.path.join("renamed_files", new_name)
                        zipf.write(file_path, new_name)
                
                # Download button
                with open(zip_path, "rb") as f:
                    st.download_button(
                        "⬇️ Download All Renamed Files",
                        f,
                        file_name="renamed_files.zip",
                        mime="application/zip"
                    )
                
                # Cleanup
                for _, new_name in renamed_files:
                    os.remove(os.path.join("renamed_files", new_name))
                os.remove(zip_path)

if __name__ == "__main__":
    main()