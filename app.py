# import os
# import streamlit as st
# from PIL import Image
# import zipfile
# from io import BytesIO
# import traceback
# import fitz  # PyMuPDF
# import tempfile
# import numpy as np
# import warnings

# # Configure page with centered layout
# st.set_page_config(
#     page_title="🖼️ Rename File Processor",
#     page_icon="✨",
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )

# # Enhanced CSS for better display
# st.markdown("""
# <style>
#     /* Main centered container */
#     .main {
#         max-width: 1200px;
#         margin: 0 auto;
#         padding: 1rem;
#     }
    
#     /* Centered header */
#     .header {
#         text-align: center;
#         margin-bottom: 2rem;
#     }
    
#     /* File upload section */
#     .upload-section {
#         display: flex;
#         justify-content: center;
#         gap: 1rem;
#         margin-bottom: 2rem;
#     }
    
#     /* File card styling */
#     .file-card {
#         border: 1px solid #e0e0e0;
#         border-radius: 10px;
#         padding: 1rem;
#         background: #f9f9f9;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.05);
#         margin-bottom: 1rem;
#     }
    
#     /* Image grid styling */
#     .image-grid {
#         display: grid;
#         grid-template-columns: repeat(3, 1fr);
#         gap: 1rem;
#         margin: 1rem 0;
#     }
    
#     .image-grid-item {
#         display: flex;
#         flex-direction: column;
#         align-items: center;
#     }
    
#     /* Image styling */
#     .stImage img {
#         border-radius: 8px;
#         box-shadow: 0 2px 6px rgba(0,0,0,0.1);
#         margin: 0.5rem auto;
#         max-width: 100%;
#         max-height: 250px;
#         object-fit: contain;
#     }
    
#     /* Button styling */
#     .stButton>button {
#         width: 100%;
#         background: linear-gradient(135deg, #6e8efb, #a777e3);
#         color: white !important;
#         font-weight: bold;
#         border: none;
#         transition: all 0.3s;
#     }
#     .stButton>button:hover {
#         transform: scale(1.02);
#         box-shadow: 0 4px 12px rgba(0,0,0,0.15);
#     }
    
#     /* Message styling */
#     .error-message {
#         color: #ff4b4b;
#         padding: 10px;
#         border-radius: 5px;
#         background-color: #ffecec;
#         margin: 10px 0;
#         text-align: center;
#     }
#     .success-message {
#         color: #00a650;
#         padding: 10px;
#         border-radius: 5px;
#         background-color: #e6f7ed;
#         margin: 10px 0;
#         text-align: center;
#     }
    
#     /* File info styling */
#     .file-info {
#         font-size: 0.9rem;
#         color: #555;
#         margin-bottom: 8px;
#         text-align: center;
#     }
    
#     /* Settings panel */
#     .settings-panel {
#         background: #f5f5f5;
#         border-radius: 10px;
#         padding: 1rem;
#         margin-bottom: 1.5rem;
#     }
    
#     /* Center align elements */
#     .center {
#         display: flex;
#         justify-content: center;
#         margin: 1rem 0;
#     }
# </style>
# """, unsafe_allow_html=True)

# def pdf_to_images(pdf_file):
#     """Convert PDF pages to PIL Images with robust temp file handling"""
#     images = []
#     temp_file_path = None
#     try:
#         # Create a temporary file to handle PDF data
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#             tmp.write(pdf_file.read())
#             temp_file_path = tmp.name
        
#         # Open the PDF file using the temporary file path
#         pdf = fitz.open(temp_file_path)
#         for page in pdf:
#             pix = page.get_pixmap(dpi=300)
#             img_data = pix.tobytes("ppm")
#             img = Image.open(BytesIO(img_data))
#             images.append((img, f"PDF_{pdf_file.name}_Page_{len(images)+1}"))
#         pdf.close()
#         return images
#     except Exception as e:
#         st.error(f"PDF conversion failed: {str(e)}")
#         return None
#     finally:
#         # Clean up temporary file
#         if temp_file_path and os.path.exists(temp_file_path):
#             try:
#                 os.unlink(temp_file_path)
#             except:
#                 pass

# def process_single_image(img, rotation, output_format, quality=95):
#     """Process a single image with rotation and format conversion"""
#     try:
#         # Apply rotation if needed
#         if rotation != 0:
#             img = img.rotate(rotation, expand=True)
        
#         # Convert to output format
#         img_bytes = BytesIO()
#         if output_format.upper() == "JPG":
#             img = img.convert("RGB")
#             img.save(img_bytes, format="JPEG", quality=quality)
#             ext = ".jpg"
#         else:
#             img.save(img_bytes, format="PNG")
#             ext = ".png"
            
#         return img, img_bytes.getvalue(), ext
    
#     except Exception as e:
#         st.error(f"Error processing image: {str(e)}")
#         st.code(traceback.format_exc())
#         return None, None, None

# def create_zip(processed_images, prefix):
#     """Create a zip file from processed images"""
#     zip_buffer = BytesIO()
#     with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
#         for idx, item in enumerate(processed_images):
#             if item["bytes"]:
#                 filename = f"{prefix}{item['new_name']}" if prefix else item['new_name']
#                 zip_file.writestr(filename, item["bytes"])
#     return zip_buffer.getvalue()

# def clear_session():
#     """Properly clear session state without popup messages"""
#     keys = list(st.session_state.keys())
#     for key in keys:
#         if key not in ["_is_running_with_streamlit"]:
#             del st.session_state[key]
#     st.rerun()

# def display_uploaded_files(uploaded_files):
#     """Display uploaded files in a grid layout"""
#     if not uploaded_files:
#         return
    
#     # Display files in a grid of 3 columns
#     cols = st.columns(3)
#     for i, file in enumerate(uploaded_files):
#         with cols[i % 3]:
#             with st.container():
#                 st.markdown('<div class="file-card">', unsafe_allow_html=True)
#                 if file.type == "application/pdf":
#                     st.markdown(f'<div class="file-info">📄 {file.name} (PDF, {file.size//1024} KB)</div>', 
#                                 unsafe_allow_html=True)
#                     st.markdown("*Contains multiple pages*")
#                 else:
#                     st.markdown(f'<div class="file-info">📄 {file.name} ({file.size//1024} KB)</div>', 
#                                 unsafe_allow_html=True)
#                     try:
#                         st.image(file, use_container_width=True)
#                     except Exception as e:
#                         st.warning(f"Couldn't display preview: {str(e)}")
#                 st.markdown('</div>', unsafe_allow_html=True)

# def main():
#     # Centered header section
#     st.markdown('<div class="header">', unsafe_allow_html=True)
#     st.title("🖼️ Rename Files Processor")
#     st.markdown("This App Developed By Rakesh Rathaur")
#     st.markdown("Process images and PDFs with automatic renaming")
#     st.markdown('</div>', unsafe_allow_html=True)
    
#     # Initialize session state for files
#     if 'uploaded_files' not in st.session_state:
#         st.session_state.uploaded_files = []
    
#     # File upload section with size validation
#     st.markdown('<div class="upload-section">', unsafe_allow_html=True)
#     new_files = st.file_uploader(
#         "📤 Upload Files (Images/PDFs)",
#         type=["jpg", "jpeg", "png", "bmp", "gif", "pdf"],
#         accept_multiple_files=True,
#         help="Supports images and multi-page PDFs (Max 50MB each)",
#         key="file_uploader"
#     )
    
#     # Validate file sizes
#     if new_files:
#         MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
#         for file in new_files:
#             if file.size > MAX_FILE_SIZE:
#                 st.error(f"File {file.name} is too large (max {MAX_FILE_SIZE//(1024*1024)}MB allowed)")
#                 st.stop()
    
#     if st.button("🔄 Refresh", help="Clear all files and start fresh", on_click=clear_session):
#         pass
#     st.markdown('</div>', unsafe_allow_html=True)
    
#     # Update session state with new files
#     if new_files:
#         st.session_state.uploaded_files = new_files
    
#     # Display uploaded files in grid
#     display_uploaded_files(st.session_state.uploaded_files)
    
#     # Main processing section
#     if st.session_state.uploaded_files:
#         # Settings panel
#         with st.expander("⚙️ Processing Settings", expanded=True):
#             st.markdown('<div class="settings-panel">', unsafe_allow_html=True)
#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 start_num = st.number_input(
#                     "Starting Number",
#                     min_value=1,
#                     value=1001,
#                     step=1,
#                     help="Starting number for sequential filenames"
#                 )
#             with col2:
#                 output_format = st.selectbox(
#                     "Output Format",
#                     ["JPG", "PNG"],
#                     index=0,
#                     help="Convert all files to selected format"
#                 )
#             with col3:
#                 jpeg_quality = st.slider(
#                     "JPEG Quality",
#                     min_value=50,
#                     max_value=100,
#                     value=95,
#                     disabled=(output_format.upper() != "JPG"),
#                     help="Higher quality means larger file size"
#                 )
#             st.markdown('</div>', unsafe_allow_html=True)
        
#         # Rotation settings
#         st.subheader("🔄 Rotation Settings")
#         rotation_values = {0: "0° (No rotation)", 90: "90°", 180: "180°", 270: "270°"}
#         global_rotation = st.selectbox(
#             "Apply this rotation to ALL files",
#             options=list(rotation_values.keys()),
#             format_func=lambda x: rotation_values[x],
#             key="global_rotation"
#         )
        
#         # Process button with error boundary
#         st.markdown('<div class="center">', unsafe_allow_html=True)
#         if st.button("✨ Process & Download All", type="primary", use_container_width=True):
#             try:
#                 with st.spinner("Processing files... Please wait"):
#                     processed_images = []
#                     progress_bar = st.progress(0)
#                     current_number = start_num
                    
#                     for i, file in enumerate(st.session_state.uploaded_files):
#                         progress_bar.progress((i + 1) / len(st.session_state.uploaded_files))
                        
#                         if file.type == "application/pdf":
#                             pdf_images = pdf_to_images(file)
#                             if pdf_images:
#                                 for img, original_name in pdf_images:
#                                     img, img_bytes, ext = process_single_image(
#                                         img,
#                                         global_rotation,
#                                         output_format,
#                                         jpeg_quality
#                                     )
#                                     if img_bytes:
#                                         new_name = f"{current_number}{ext}"
#                                         processed_images.append({
#                                             "original": original_name,
#                                             "new_name": new_name,
#                                             "image": img,
#                                             "bytes": img_bytes
#                                         })
#                                         current_number += 1
#                         else:
#                             try:
#                                 img = Image.open(file)
#                                 img, img_bytes, ext = process_single_image(
#                                     img,
#                                     global_rotation,
#                                     output_format,
#                                     jpeg_quality
#                                 )
#                                 if img_bytes:
#                                     new_name = f"{current_number}{ext}"
#                                     processed_images.append({
#                                         "original": file.name,
#                                         "new_name": new_name,
#                                         "image": img,
#                                         "bytes": img_bytes
#                                     })
#                                     current_number += 1
#                             except Exception as e:
#                                 st.error(f"Failed to process {file.name}: {str(e)}")
                    
#                     progress_bar.empty()
                    
#                     if processed_images:
#                         # Create zip file
#                         prefix = st.text_input("Filename prefix (optional)", value="", key="prefix_input")
#                         zip_data = create_zip(processed_images, prefix)
                        
#                         # Show success message
#                         st.markdown(
#                             f'<div class="success-message">✅ Successfully processed {len(processed_images)} files!</div>',
#                             unsafe_allow_html=True
#                         )
                        
#                         # Show previews in a grid of 3 columns
#                         st.subheader("🖼️ Processed Results")
                        
#                         # Display images in a grid of 3 columns
#                         cols = st.columns(3)
#                         for i, item in enumerate(processed_images):
#                             with cols[i % 3]:
#                                 st.image(
#                                     item["image"],
#                                     caption=f"{item['new_name']} (From: {item['original']})",
#                                     use_container_width=True
#                                 )
                        
#                         # Download button
#                         st.markdown('<div class="center">', unsafe_allow_html=True)
#                         st.download_button(
#                             label="📥 Download Processed Files (ZIP)",
#                             data=zip_data,
#                             file_name="processed_files.zip",
#                             mime="application/zip",
#                             use_container_width=True
#                         )
#                         st.markdown('</div>', unsafe_allow_html=True)
#                     else:
#                         st.markdown(
#                             '<div class="error-message">❌ No files were processed successfully</div>',
#                             unsafe_allow_html=True
#                         )
#             except Exception as e:
#                 st.error(f"An unexpected error occurred: {str(e)}")
#                 st.code(traceback.format_exc())
#         st.markdown('</div>', unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()