# import os
# import streamlit as st
# from PIL import Image
# import zipfile
# from io import BytesIO

# # Configure page
# st.set_page_config(page_title="🖼️ Image Renamer Pro", page_icon="🖼️", layout="wide")

# # Custom CSS for better UI
# st.markdown("""
# <style>
#     .stImage img {
#         border-radius: 10px;
#         box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
#     }
#     .stDownloadButton button {
#         width: 100%;
#         background-color: #4CAF50 !important;
#         color: white !important;
#     }
#     .stFileUploader div {
#         padding: 20px;
#         border: 2px dashed #ccc;
#         border-radius: 5px;
#     }
# </style>
# """, unsafe_allow_html=True)

# def process_images(uploaded_files, start_num, rotation_angles):
#     """Process and rename images with rotation"""
#     processed_images = []
    
#     for i, uploaded_file in enumerate(uploaded_files, start=start_num):
#         try:
#             img = Image.open(uploaded_file)
            
#             # Apply rotation if specified
#             if uploaded_file.name in rotation_angles:
#                 img = img.rotate(rotation_angles[uploaded_file.name], expand=True)
            
#             # Convert to RGB if needed (for JPEG compatibility)
#             if img.mode in ('RGBA', 'P'):
#                 img = img.convert('RGB')
                
#             # Save to bytes
#             img_bytes = BytesIO()
#             img.save(img_bytes, format='JPEG' if uploaded_file.name.lower().endswith('.jpg') else 'PNG')
            
#             # Create new filename
#             ext = os.path.splitext(uploaded_file.name)[1].lower()
#             new_name = f"{i}{ext}"
            
#             processed_images.append({
#                 "original": uploaded_file.name,
#                 "new_name": new_name,
#                 "image": img,
#                 "bytes": img_bytes.getvalue()
#             })
#         except Exception as e:
#             st.warning(f"Couldn't process {uploaded_file.name}: {str(e)}")
    
#     return processed_images

# def main():
#     st.title("🖼️ Image Processor Pro")
#     st.markdown("Upload images, preview, rotate if needed, and download renamed files")
    
#     col1, col2 = st.columns([1, 2])
    
#     with col1:
#         # File uploader
#         uploaded_files = st.file_uploader(
#             "Choose images",
#             type=["jpg", "jpeg", "png", "bmp", "gif"],
#             accept_multiple_files=True,
#             key="file_uploader"
#         )
        
#         # Starting number input
#         start_num = st.number_input(
#             "Starting number", 
#             min_value=1,
#             value=1001,
#             step=1
#         )
        
#         # Custom prefix
#         custom_prefix = st.text_input("Custom prefix (optional)")
    
#     # Rotation controls
#     rotation_angles = {}
#     if uploaded_files:
#         st.subheader("🔄 Image Rotation")
#         cols = st.columns(4)
        
#         for i, uploaded_file in enumerate(uploaded_files):
#             with cols[i % 4]:
#                 st.image(uploaded_file, use_column_width=True)
#                 rotation_angles[uploaded_file.name] = st.slider(
#                     f"Rotate {uploaded_file.name}",
#                     -180, 180, 0,
#                     key=f"rotate_{uploaded_file.name}"
#                 )
    
#     # Process and download
#     if uploaded_files and st.button("🛠️ Process Images", type="primary"):
#         with st.spinner("Processing images..."):
#             processed = process_images(uploaded_files, start_num, rotation_angles)
            
#             if processed:
#                 st.success(f"✅ Processed {len(processed)} images!")
                
#                 # Create ZIP
#                 zip_buffer = BytesIO()
#                 with zipfile.ZipFile(zip_buffer, "w") as zip_file:
#                     for item in processed:
#                         filename = f"{custom_prefix}_{item['new_name']}" if custom_prefix else item['new_name']
#                         zip_file.writestr(filename, item["bytes"])
                
#                 # Show processed images
#                 st.subheader("🖼️ Processed Images Preview")
#                 preview_cols = st.columns(4)
#                 for i, item in enumerate(processed):
#                     with preview_cols[i % 4]:
#                         st.image(item["image"], caption=item["new_name"], use_column_width=True)
                
#                 # Download button
#                 st.download_button(
#                     label="📥 Download All Images",
#                     data=zip_buffer.getvalue(),
#                     file_name="processed_images.zip",
#                     mime="application/zip",
#                     key="download_zip"
#                 )

# if __name__ == "__main__":
#     main()












# import os
# import streamlit as st
# from PIL import Image, ImageOps
# import zipfile
# from io import BytesIO
# import traceback

# # Configure page with centered layout
# st.set_page_config(
#     page_title="🖼️ Image Rename Processor",
#     page_icon="✨",
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )

# # Custom CSS for improved UI
# st.markdown("""
# <style>
#     .main {
#         max-width: 800px;
#         padding: 2rem;
#         margin: auto;
#     }
#     .stImage img {
#         border-radius: 10px;
#         box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
#         margin: 0.5rem auto;
#         max-width: 100%;
#         max-height: 300px;
#         object-fit: contain;
#     }
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
#         box-shadow: 0 4px 12px 0 rgba(0,0,0,0.2);
#     }
#     .error-message {
#         color: #ff4b4b;
#         padding: 10px;
#         border-radius: 5px;
#         background-color: #ffecec;
#         margin: 10px 0;
#     }
#     .success-message {
#         color: #00a650;
#         padding: 10px;
#         border-radius: 5px;
#         background-color: #e6f7ed;
#         margin: 10px 0;
#     }
#     .rotate-option {
#         padding: 8px 12px;
#         border-radius: 8px;
#         margin: 5px 0;
#     }
#     .file-info {
#         font-size: 0.9rem;
#         color: #666;
#         margin-bottom: 5px;
#     }
# </style>
# """, unsafe_allow_html=True)

# def validate_image(file):
#     """Validate if the file is a proper image"""
#     try:
#         Image.open(file)
#         return True
#     except:
#         return False

# def process_single_image(file, rotation, output_format, quality=95):
#     """Process a single image with rotation and format conversion"""
#     try:
#         img = Image.open(file)
        
#         # Apply rotation if needed
#         if rotation != 0:
#             img = img.rotate(rotation, expand=True)
        
#         # Convert to output format
#         img_bytes = BytesIO()
#         if output_format == "JPEG":
#             img = img.convert("RGB")
#             img.save(img_bytes, format="JPEG", quality=quality)
#             ext = ".jpg"
#         else:
#             img.save(img_bytes, format="PNG")
#             ext = ".png"
            
#         return img, img_bytes.getvalue(), ext
    
#     except Exception as e:
#         st.error(f"Error processing {file.name}: {str(e)}")
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

# def main():
#     # Centered header
#     st.markdown('<div class="header">', unsafe_allow_html=True)
#     st.title("🖼️ Image Rename Processor")
#     st.markdown("This App Devloped By Rakesh Rathaur")
#     st.markdown("Upload, transform, and download images in batch with ease")
#     st.markdown('</div>', unsafe_allow_html=True)
    
#     # File upload section
#     uploaded_files = st.file_uploader(
#         "📤 Upload Images (JPG, PNG, BMP, GIF)",
#         type=["jpg", "jpeg", "png", "bmp", "gif"],
#         accept_multiple_files=True,
#         help="Maximum 20 images at once (for better performance)"
#     )
    
#     if uploaded_files:
#         # Limit to 20 files for performance
#         if len(uploaded_files) > 20:
#             st.warning("For best performance, please upload 20 images or fewer")
#             uploaded_files = uploaded_files[:20]
        
#         # Settings panel
#         with st.expander("⚙️ Processing Settings", expanded=True):
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
#                     help="Convert all images to selected format"
#                 )
#             with col3:
#                 jpeg_quality = st.slider(
#                     "JPEG Quality",
#                     min_value=50,
#                     max_value=100,
#                     value=95,
#                     disabled=(output_format != "JPEG"),
#                     help="Higher quality means larger file size"
#                 )
        
#         # Rotation controls
#         st.subheader("🔄 Rotation Settings")
#         st.markdown("Select rotation for each image:")
        
#         rotation_values = {0: "0° (No rotation)", 90: "90°", 180: "180°", 270: "270°"}
#         # rotation_values = {0: "90°"}

#         rotation_choices = {}
        
#         # Display images in a responsive grid
#         cols = st.columns(2)
#         for i, file in enumerate(uploaded_files):
#             with cols[i % 2]:
#                 # File info
#                 st.markdown(f'<div class="file-info">📄 {file.name} ({file.size//1024} KB)</div>', 
#                           unsafe_allow_html=True)
                
#                 # Preview with max height
#                 try:
#                     st.image(file, use_container_width=True)  # Updated parameter
#                 except:
#                     st.warning("Couldn't display preview")
                
#                 # Rotation selector
#                 rotation_choices[file.name] = st.selectbox(
#                     f"Rotation for {file.name}",
#                     options=list(rotation_values.keys()),
#                     format_func=lambda x: rotation_values[x],
#                     key=f"rotate_{file.name}"
#                 )
        
#         # Process button
#         if st.button("✨ Process & Download All", type="primary", use_container_width=True):
#             with st.spinner("Processing images... Please wait"):
#                 processed_images = []
#                 progress_bar = st.progress(0)
                
#                 for i, file in enumerate(uploaded_files):
#                     # Update progress
#                     progress_bar.progress((i + 1) / len(uploaded_files))
                    
#                     # Process each image
#                     img, img_bytes, ext = process_single_image(
#                         file,
#                         rotation_choices[file.name],
#                         output_format,
#                         jpeg_quality
#                     )
                    
#                     if img_bytes:
#                         new_name = f"{start_num + i}{ext}"
#                         processed_images.append({
#                             "original": file.name,
#                             "new_name": new_name,
#                             "image": img,
#                             "bytes": img_bytes
#                         })
                
#                 if processed_images:
#                     # Create zip file
#                     prefix = st.text_input("Filename prefix (optional)", value="")
#                     zip_data = create_zip(processed_images, prefix)
                    
#                     # Show success message
#                     st.markdown(
#                         f'<div class="success-message">✅ Successfully processed {len(processed_images)} images!</div>',
#                         unsafe_allow_html=True
#                     )
                    
#                     # Show previews
#                     st.subheader("🖼️ Processed Results")
#                     preview_cols = st.columns(2)
#                     for i, item in enumerate(processed_images):
#                         with preview_cols[i % 2]:
#                             st.image(
#                                 item["image"],
#                                 caption=f"{item['new_name']} ({rotation_values[rotation_choices[item['original']]]})",
#                                 use_container_width=True  # Updated parameter
#                             )
                    
#                     # Download button
#                     st.download_button(
#                         label="📥 Download Processed Images (ZIP)",
#                         data=zip_data,
#                         file_name="processed_images.zip",
#                         mime="application/zip",
#                         use_container_width=True
#                     )
#                 else:
#                     st.markdown(
#                         '<div class="error-message">❌ No images were processed successfully</div>',
#                         unsafe_allow_html=True
#                     )
                
#                 progress_bar.empty()

# if __name__ == "__main__":
#     main()




























































































# import os
# import streamlit as st
# from PIL import Image, ImageOps
# import zipfile
# from io import BytesIO
# import traceback
# import fitz  # PyMuPDF

# # Configure page with centered layout
# st.set_page_config(
#     page_title="🖼️ Rename Images Processor (Images + PDFs)",
#     page_icon="✨",
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )

# # Custom CSS for improved UI
# st.markdown("""
# <style>
#     .main {
#         max-width: 800px;
#         padding: 2rem;
#         margin: auto;
#     }
#     .stImage img {
#         border-radius: 10px;
#         box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
#         margin: 0.5rem auto;
#         max-width: 100%;
#         max-height: 300px;
#         object-fit: contain;
#     }
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
#         box-shadow: 0 4px 12px 0 rgba(0,0,0,0.2);
#     }
#     .error-message {
#         color: #ff4b4b;
#         padding: 10px;
#         border-radius: 5px;
#         background-color: #ffecec;
#         margin: 10px 0;
#     }
#     .success-message {
#         color: #00a650;
#         padding: 10px;
#         border-radius: 5px;
#         background-color: #e6f7ed;
#         margin: 10px 0;
#     }
#     .rotate-option {
#         padding: 8px 12px;
#         border-radius: 8px;
#         margin: 5px 0;
#     }
#     .file-info {
#         font-size: 0.9rem;
#         color: #666;
#         margin-bottom: 5px;
#     }
# </style>
# """, unsafe_allow_html=True)

# def pdf_to_images(pdf_file):
#     """Convert PDF pages to PIL Images"""
#     images = []
#     try:
#         pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")
#         for page in pdf:
#             pix = page.get_pixmap(dpi=300)
#             img_data = pix.tobytes("ppm")
#             img = Image.open(BytesIO(img_data))
#             images.append((img, f"PDF_{pdf_file.name}_Page_{len(images)+1}"))
#         return images
#     except Exception as e:
#         st.error(f"PDF conversion failed: {str(e)}")
#         return None

# def validate_image(file):
#     """Validate if the file is a proper image"""
#     try:
#         Image.open(file)
#         return True
#     except:
#         return False

# def process_single_image(img, rotation, output_format, quality=95):
#     """Process a single image with rotation and format conversion"""
#     try:
#         # Apply rotation if needed
#         if rotation != 0:
#             img = img.rotate(rotation, expand=True)
        
#         # Convert to output format
#         img_bytes = BytesIO()
#         if output_format == "JPEG":
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

# def main():
#     # Centered header
#     st.markdown('<div class="header">', unsafe_allow_html=True)
#     st.title("🖼️ Advanced File Processor")
#     st.markdown("This App Devloped By Rakesh Rathaur")
#     st.markdown("Process images and PDFs with automatic renaming")
#     st.markdown('</div>', unsafe_allow_html=True)
    
#     # File upload section
#     uploaded_files = st.file_uploader(
#         "📤 Upload Files (Images/PDFs)",
#         type=["jpg", "jpeg", "png", "bmp", "gif", "pdf"],
#         accept_multiple_files=True,
#         help="Supports images and multi-page PDFs"
#     )
    
#     if uploaded_files:
#         # Settings panel
#         with st.expander("⚙️ Processing Settings", expanded=True):
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
#                     disabled=(output_format != "JPEG"),
#                     help="Higher quality means larger file size"
#                 )
        
#         # Rotation controls
#         st.subheader("🔄 Rotation Settings")
#         rotation_values = {0: "0° (No rotation)", 90: "90°", 180: "180°", 270: "270°"}
#         rotation_choices = {}
        
#         # Display files in a responsive grid
#         cols = st.columns(2)
#         file_counter = 0
#         for file in uploaded_files:
#             with cols[file_counter % 2]:
#                 if file.type == "application/pdf":
#                     st.markdown(f'<div class="file-info">📄 {file.name} (PDF, {file.size//1024} KB)</div>', 
#                               unsafe_allow_html=True)
#                     st.markdown("*Contains multiple pages*")
#                     rotation_choices[file.name] = st.selectbox(
#                         f"Rotation for {file.name}",
#                         options=list(rotation_values.keys()),
#                         format_func=lambda x: rotation_values[x],
#                         key=f"rotate_pdf_{file.name}"
#                     )
#                 else:
#                     st.markdown(f'<div class="file-info">📄 {file.name} ({file.size//1024} KB)</div>', 
#                               unsafe_allow_html=True)
#                     try:
#                         st.image(file, use_container_width=True)
#                     except:
#                         st.warning("Couldn't display preview")
#                     rotation_choices[file.name] = st.selectbox(
#                         f"Rotation for {file.name}",
#                         options=list(rotation_values.keys()),
#                         format_func=lambda x: rotation_values[x],
#                         key=f"rotate_{file.name}"
#                     )
#                 file_counter += 1
        
#         # Process button
#         if st.button("✨ Process & Download All", type="primary", use_container_width=True):
#             with st.spinner("Processing files... Please wait"):
#                 processed_images = []
#                 progress_bar = st.progress(0)
#                 current_number = start_num
                
#                 for i, file in enumerate(uploaded_files):
#                     # Update progress
#                     progress_bar.progress((i + 1) / len(uploaded_files))
                    
#                     if file.type == "application/pdf":
#                         pdf_images = pdf_to_images(file)
#                         if pdf_images:
#                             for img, original_name in pdf_images:
#                                 img, img_bytes, ext = process_single_image(
#                                     img,
#                                     rotation_choices[file.name],
#                                     output_format,
#                                     jpeg_quality
#                                 )
#                                 if img_bytes:
#                                     new_name = f"{current_number}{ext}"
#                                     processed_images.append({
#                                         "original": original_name,
#                                         "new_name": new_name,
#                                         "image": img,
#                                         "bytes": img_bytes
#                                     })
#                                     current_number += 1
#                     else:
#                         img = Image.open(file)
#                         img, img_bytes, ext = process_single_image(
#                             img,
#                             rotation_choices[file.name],
#                             output_format,
#                             jpeg_quality
#                         )
#                         if img_bytes:
#                             new_name = f"{current_number}{ext}"
#                             processed_images.append({
#                                 "original": file.name,
#                                 "new_name": new_name,
#                                 "image": img,
#                                 "bytes": img_bytes
#                             })
#                             current_number += 1
                
#                 if processed_images:
#                     # Create zip file
#                     prefix = st.text_input("Filename prefix (optional)", value="")
#                     zip_data = create_zip(processed_images, prefix)
                    
#                     # Show success message
#                     st.markdown(
#                         f'<div class="success-message">✅ Successfully processed {len(processed_images)} files!</div>',
#                         unsafe_allow_html=True
#                     )
                    
#                     # Show previews
#                     st.subheader("🖼️ Processed Results")
#                     preview_cols = st.columns(2)
#                     for i, item in enumerate(processed_images):
#                         with preview_cols[i % 2]:
#                             st.image(
#                                 item["image"],
#                                 caption=f"{item['new_name']} (From: {item['original']})",
#                                 use_container_width=True
#                             )
                    
#                     # Download button
#                     st.download_button(
#                         label="📥 Download Processed Files (ZIP)",
#                         data=zip_data,
#                         file_name="processed_files.zip",
#                         mime="application/zip",
#                         use_container_width=True
#                     )
#                 else:
#                     st.markdown(
#                         '<div class="error-message">❌ No files were processed successfully</div>',
#                         unsafe_allow_html=True
#                     )
                
#                 progress_bar.empty()

# if __name__ == "__main__":
#     main()








































































































































































































# import os
# import streamlit as st
# from PIL import Image, ImageOps
# import zipfile
# from io import BytesIO
# import traceback
# import fitz  # PyMuPDF

# # Configure page with centered layout
# st.set_page_config(
#     page_title="🖼️ Rename File Processor",
#     page_icon="✨",
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )

# # Custom CSS for improved UI
# st.markdown("""
# <style>
#     .main {
#         max-width: 800px;
#         padding: 2rem;
#         margin: auto;
#     }
#     .stImage img {
#         border-radius: 10px;
#         box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
#         margin: 0.5rem auto;
#         max-width: 100%;
#         max-height: 300px;
#         object-fit: contain;
#     }
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
#         box-shadow: 0 4px 12px 0 rgba(0,0,0,0.2);
#     }
#     .error-message {
#         color: #ff4b4b;
#         padding: 10px;
#         border-radius: 5px;
#         background-color: #ffecec;
#         margin: 10px 0;
#     }
#     .success-message {
#         color: #00a650;
#         padding: 10px;
#         border-radius: 5px;
#         background-color: #e6f7ed;
#         margin: 10px 0;
#     }
#     .rotate-option {
#         padding: 8px 12px;
#         border-radius: 8px;
#         margin: 5px 0;
#     }
#     .file-info {
#         font-size: 0.9rem;
#         color: #666;
#         margin-bottom: 5px;
#     }
#     .refresh-btn {
#         margin-left: 10px;
#     }
# </style>
# """, unsafe_allow_html=True)

# def pdf_to_images(pdf_file):
#     """Convert PDF pages to PIL Images"""
#     images = []
#     try:
#         pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")
#         for page in pdf:
#             pix = page.get_pixmap(dpi=300)
#             img_data = pix.tobytes("ppm")
#             img = Image.open(BytesIO(img_data))
#             images.append((img, f"PDF_{pdf_file.name}_Page_{len(images)+1}"))
#         return images
#     except Exception as e:
#         st.error(f"PDF conversion failed: {str(e)}")
#         return None

# def validate_image(file):
#     """Validate if the file is a proper image"""
#     try:
#         Image.open(file)
#         return True
#     except:
#         return False

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
#     """Clear all files from session state and reset"""
#     st.session_state.uploaded_files = []
#     st.session_state.file_uploader = []
#     st.experimental_rerun()

# def main():
#     # Centered header
#     st.markdown('<div class="header">', unsafe_allow_html=True)
#     st.title("🖼️ Rename Files Processor")
#     st.markdown("This App Developed By Rakesh Rathaur")
#     st.markdown("Process images and PDFs with automatic renaming")
#     st.markdown('</div>', unsafe_allow_html=True)
    
#     # Initialize session state for files if not exists
#     if 'uploaded_files' not in st.session_state:
#         st.session_state.uploaded_files = []
    
#     # File upload section with refresh button
#     col1, col2 = st.columns([4, 1])
#     with col1:
#         new_files = st.file_uploader(
#             "📤 Upload Files (Images/PDFs)",
#             type=["jpg", "jpeg", "png", "bmp", "gif", "pdf"],
#             accept_multiple_files=True,
#             help="Supports images and multi-page PDFs",
#             key="file_uploader"
#         )
#     with col2:
#         if st.button("🔄 Refresh", key="refresh_btn", help="Clear all files and start fresh", 
#                     on_click=clear_session):
#             pass
    
#     # Update session state with new files
#     if new_files:
#         st.session_state.uploaded_files = new_files
    
#     if st.session_state.uploaded_files:
#         # Settings panel
#         with st.expander("⚙️ Processing Settings", expanded=True):
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
#                     index=0,  # Default to JPG
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
        
#         # Global rotation control
#         st.subheader("🔄 Rotation Settings")
#         rotation_values = {0: "0° (No rotation)", 90: "90°", 180: "180°", 270: "270°"}
        
#         # Add global rotation control
#         global_rotation = st.selectbox(
#             "Apply this rotation to ALL files",
#             options=list(rotation_values.keys()),
#             format_func=lambda x: rotation_values[x],
#             key="global_rotation"
#         )
        
#         # Individual rotation overrides
#         st.markdown("**Individual adjustments (optional):**")
#         rotation_choices = {}
        
#         # Display files in a responsive grid
#         cols = st.columns(2)
#         file_counter = 0
#         for file in st.session_state.uploaded_files:
#             with cols[file_counter % 2]:
#                 if file.type == "application/pdf":
#                     st.markdown(f'<div class="file-info">📄 {file.name} (PDF, {file.size//1024} KB)</div>', 
#                               unsafe_allow_html=True)
#                     st.markdown("*Contains multiple pages*")
#                     rotation_choices[file.name] = st.selectbox(
#                         f"Rotation for {file.name}",
#                         options=list(rotation_values.keys()),
#                         format_func=lambda x: rotation_values[x],
#                         index=list(rotation_values.keys()).index(global_rotation),
#                         key=f"rotate_pdf_{file.name}"
#                     )
#                 else:
#                     st.markdown(f'<div class="file-info">📄 {file.name} ({file.size//1024} KB)</div>', 
#                               unsafe_allow_html=True)
#                     try:
#                         st.image(file, use_column_width=True)
#                     except:
#                         st.warning("Couldn't display preview")
#                     rotation_choices[file.name] = st.selectbox(
#                         f"Rotation for {file.name}",
#                         options=list(rotation_values.keys()),
#                         format_func=lambda x: rotation_values[x],
#                         index=list(rotation_values.keys()).index(global_rotation),
#                         key=f"rotate_{file.name}"
#                     )
#                 file_counter += 1
        
#         # Process button
#         if st.button("✨ Process & Download All", type="primary", use_container_width=True):
#             with st.spinner("Processing files... Please wait"):
#                 processed_images = []
#                 progress_bar = st.progress(0)
#                 current_number = start_num
                
#                 for i, file in enumerate(st.session_state.uploaded_files):
#                     # Update progress
#                     progress_bar.progress((i + 1) / len(st.session_state.uploaded_files))
                    
#                     if file.type == "application/pdf":
#                         pdf_images = pdf_to_images(file)
#                         if pdf_images:
#                             for img, original_name in pdf_images:
#                                 img, img_bytes, ext = process_single_image(
#                                     img,
#                                     rotation_choices.get(file.name, global_rotation),
#                                     output_format,
#                                     jpeg_quality
#                                 )
#                                 if img_bytes:
#                                     new_name = f"{current_number}{ext}"
#                                     processed_images.append({
#                                         "original": original_name,
#                                         "new_name": new_name,
#                                         "image": img,
#                                         "bytes": img_bytes
#                                     })
#                                     current_number += 1
#                     else:
#                         try:
#                             img = Image.open(file)
#                             img, img_bytes, ext = process_single_image(
#                                 img,
#                                 rotation_choices.get(file.name, global_rotation),
#                                 output_format,
#                                 jpeg_quality
#                             )
#                             if img_bytes:
#                                 new_name = f"{current_number}{ext}"
#                                 processed_images.append({
#                                     "original": file.name,
#                                     "new_name": new_name,
#                                     "image": img,
#                                     "bytes": img_bytes
#                                 })
#                                 current_number += 1
#                         except Exception as e:
#                             st.error(f"Failed to process {file.name}: {str(e)}")
                
#                 if processed_images:
#                     # Create zip file
#                     prefix = st.text_input("Filename prefix (optional)", value="")
#                     zip_data = create_zip(processed_images, prefix)
                    
#                     # Show success message
#                     st.markdown(
#                         f'<div class="success-message">✅ Successfully processed {len(processed_images)} files!</div>',
#                         unsafe_allow_html=True
#                     )
                    
#                     # Show previews
#                     st.subheader("🖼️ Processed Results")
#                     preview_cols = st.columns(2)
#                     for i, item in enumerate(processed_images):
#                         with preview_cols[i % 2]:
#                             st.image(
#                                 item["image"],
#                                 caption=f"{item['new_name']} (From: {item['original']})",
#                                 use_column_width=True
#                             )
                    
#                     # Download button
#                     st.download_button(
#                         label="📥 Download Processed Files (ZIP)",
#                         data=zip_data,
#                         file_name="processed_files.zip",
#                         mime="application/zip",
#                         use_container_width=True
#                     )
#                 else:
#                     st.markdown(
#                         '<div class="error-message">❌ No files were processed successfully</div>',
#                         unsafe_allow_html=True
#                     )
                
#                 progress_bar.empty()

# if __name__ == "__main__":
#     main()
































































import os
import streamlit as st
from PIL import Image, ImageOps
import zipfile
from io import BytesIO
import traceback
import fitz  # PyMuPDF

# Configure page with centered layout
st.set_page_config(
    page_title="🖼️ Rename File Processor",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for improved UI
st.markdown("""
<style>
    .main {
        max-width: 800px;
        padding: 2rem;
        margin: auto;
    }
    .stImage img {
        border-radius: 10px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        margin: 0.5rem auto;
        max-width: 100%;
        max-height: 300px;
        object-fit: contain;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #6e8efb, #a777e3);
        color: white !important;
        font-weight: bold;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px 0 rgba(0,0,0,0.2);
    }
    .error-message {
        color: #ff4b4b;
        padding: 10px;
        border-radius: 5px;
        background-color: #ffecec;
        margin: 10px 0;
    }
    .success-message {
        color: #00a650;
        padding: 10px;
        border-radius: 5px;
        background-color: #e6f7ed;
        margin: 10px 0;
    }
    .rotate-option {
        padding: 8px 12px;
        border-radius: 8px;
        margin: 5px 0;
    }
    .file-info {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 5px;
    }
    .refresh-btn {
        margin-left: 10px;
    }
</style>
""", unsafe_allow_html=True)

def pdf_to_images(pdf_file):
    """Convert PDF pages to PIL Images"""
    images = []
    try:
        pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")
        for page in pdf:
            pix = page.get_pixmap(dpi=300)
            img_data = pix.tobytes("ppm")
            img = Image.open(BytesIO(img_data))
            images.append((img, f"PDF_{pdf_file.name}_Page_{len(images)+1}"))
        return images
    except Exception as e:
        st.error(f"PDF conversion failed: {str(e)}")
        return None

def validate_image(file):
    """Validate if the file is a proper image"""
    try:
        Image.open(file)
        return True
    except:
        return False

def process_single_image(img, rotation, output_format, quality=95):
    """Process a single image with rotation and format conversion"""
    try:
        # Apply rotation if needed
        if rotation != 0:
            img = img.rotate(rotation, expand=True)
        
        # Convert to output format
        img_bytes = BytesIO()
        if output_format.upper() == "JPG":
            img = img.convert("RGB")
            img.save(img_bytes, format="JPEG", quality=quality)
            ext = ".jpg"
        else:
            img.save(img_bytes, format="PNG")
            ext = ".png"
            
        return img, img_bytes.getvalue(), ext
    
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        st.code(traceback.format_exc())
        return None, None, None

def create_zip(processed_images, prefix):
    """Create a zip file from processed images"""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for idx, item in enumerate(processed_images):
            if item["bytes"]:
                filename = f"{prefix}{item['new_name']}" if prefix else item['new_name']
                zip_file.writestr(filename, item["bytes"])
    return zip_buffer.getvalue()

def clear_session():
    """Clear all files from session state and reset"""
    st.session_state.uploaded_files = []
    st.rerun()

def main():
    # Centered header
    st.markdown('<div class="header">', unsafe_allow_html=True)
    st.title("🖼️ Rename Files Processor")
    st.markdown("This App Developed By Rakesh Rathaur")
    st.markdown("Process images and PDFs with automatic renaming")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Initialize session state for files if not exists
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    
    # File upload section with refresh button
    col1, col2 = st.columns([4, 1])
    with col1:
        new_files = st.file_uploader(
            "📤 Upload Files (Images/PDFs)",
            type=["jpg", "jpeg", "png", "bmp", "gif", "pdf"],
            accept_multiple_files=True,
            help="Supports images and multi-page PDFs",
            key="file_uploader"
        )
    with col2:
        if st.button("🔄 Refresh", key="refresh_btn", help="Clear all files and start fresh", 
                    on_click=clear_session):
            pass
    
    # Update session state with new files
    if new_files:
        st.session_state.uploaded_files = new_files
    
    if st.session_state.uploaded_files:
        # Settings panel
        with st.expander("⚙️ Processing Settings", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                start_num = st.number_input(
                    "Starting Number",
                    min_value=1,
                    value=1001,
                    step=1,
                    help="Starting number for sequential filenames"
                )
            with col2:
                output_format = st.selectbox(
                    "Output Format",
                    ["JPG", "PNG"],
                    index=0,  # Default to JPG
                    help="Convert all files to selected format"
                )
            with col3:
                jpeg_quality = st.slider(
                    "JPEG Quality",
                    min_value=50,
                    max_value=100,
                    value=95,
                    disabled=(output_format.upper() != "JPG"),
                    help="Higher quality means larger file size"
                )
        
        # Global rotation control
        st.subheader("🔄 Rotation Settings")
        rotation_values = {0: "0° (No rotation)", 90: "90°", 180: "180°", 270: "270°"}
        
        # Add global rotation control
        global_rotation = st.selectbox(
            "Apply this rotation to ALL files",
            options=list(rotation_values.keys()),
            format_func=lambda x: rotation_values[x],
            key="global_rotation"
        )
        
        # Individual rotation overrides
        st.markdown("**Individual adjustments (optional):**")
        rotation_choices = {}
        
        # Display files in a responsive grid
        cols = st.columns(2)
        file_counter = 0
        for file in st.session_state.uploaded_files:
            with cols[file_counter % 2]:
                if file.type == "application/pdf":
                    st.markdown(f'<div class="file-info">📄 {file.name} (PDF, {file.size//1024} KB)</div>', 
                              unsafe_allow_html=True)
                    st.markdown("*Contains multiple pages*")
                    rotation_choices[file.name] = st.selectbox(
                        f"Rotation for {file.name}",
                        options=list(rotation_values.keys()),
                        format_func=lambda x: rotation_values[x],
                        index=list(rotation_values.keys()).index(global_rotation),
                        key=f"rotate_pdf_{file.name}"
                    )
                else:
                    st.markdown(f'<div class="file-info">📄 {file.name} ({file.size//1024} KB)</div>', 
                              unsafe_allow_html=True)
                    try:
                        st.image(file, use_column_width=True)
                    except:
                        st.warning("Couldn't display preview")
                    rotation_choices[file.name] = st.selectbox(
                        f"Rotation for {file.name}",
                        options=list(rotation_values.keys()),
                        format_func=lambda x: rotation_values[x],
                        index=list(rotation_values.keys()).index(global_rotation),
                        key=f"rotate_{file.name}"
                    )
                file_counter += 1
        
        # Process button
        if st.button("✨ Process & Download All", type="primary", use_container_width=True):
            with st.spinner("Processing files... Please wait"):
                processed_images = []
                progress_bar = st.progress(0)
                current_number = start_num
                
                for i, file in enumerate(st.session_state.uploaded_files):
                    # Update progress
                    progress_bar.progress((i + 1) / len(st.session_state.uploaded_files))
                    
                    if file.type == "application/pdf":
                        pdf_images = pdf_to_images(file)
                        if pdf_images:
                            for img, original_name in pdf_images:
                                img, img_bytes, ext = process_single_image(
                                    img,
                                    rotation_choices.get(file.name, global_rotation),
                                    output_format,
                                    jpeg_quality
                                )
                                if img_bytes:
                                    new_name = f"{current_number}{ext}"
                                    processed_images.append({
                                        "original": original_name,
                                        "new_name": new_name,
                                        "image": img,
                                        "bytes": img_bytes
                                    })
                                    current_number += 1
                    else:
                        try:
                            img = Image.open(file)
                            img, img_bytes, ext = process_single_image(
                                img,
                                rotation_choices.get(file.name, global_rotation),
                                output_format,
                                jpeg_quality
                            )
                            if img_bytes:
                                new_name = f"{current_number}{ext}"
                                processed_images.append({
                                    "original": file.name,
                                    "new_name": new_name,
                                    "image": img,
                                    "bytes": img_bytes
                                })
                                current_number += 1
                        except Exception as e:
                            st.error(f"Failed to process {file.name}: {str(e)}")
                
                if processed_images:
                    # Create zip file
                    prefix = st.text_input("Filename prefix (optional)", value="")
                    zip_data = create_zip(processed_images, prefix)
                    
                    # Show success message
                    st.markdown(
                        f'<div class="success-message">✅ Successfully processed {len(processed_images)} files!</div>',
                        unsafe_allow_html=True
                    )
                    
                    # Show previews
                    st.subheader("🖼️ Processed Results")
                    preview_cols = st.columns(2)
                    for i, item in enumerate(processed_images):
                        with preview_cols[i % 2]:
                            st.image(
                                item["image"],
                                caption=f"{item['new_name']} (From: {item['original']})",
                                use_column_width=True
                            )
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Processed Files (ZIP)",
                        data=zip_data,
                        file_name="processed_files.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
                else:
                    st.markdown(
                        '<div class="error-message">❌ No files were processed successfully</div>',
                        unsafe_allow_html=True
                    )
                
                progress_bar.empty()

if __name__ == "__main__":
    main()
