from PIL import Image, ImageFilter

def crop_scale_blur_overlay_correct_position_and_final_crop(image_path, output_base_path):
    # 打开图片
    image = Image.open(image_path)
    original_size = image.size

    # 计算裁剪区域，保持宽度不变
    width, height = image.size
    new_height = int(height * 1/3)
    top = (height - new_height) // 2
    bottom = (height + new_height) // 2

    # 裁剪图片，并保存
    image_cropped = image.crop((0, top, width, bottom))
    image_cropped.save(f'{output_base_path}_cropped.jpg')

    # 等比例放大图片，并保存
    scale_factor = original_size[1] / new_height
    scaled_width = int(width * scale_factor)
    scaled_height = original_size[1]  # 直接使用原图高度作为目标高度

    image_scaled = image_cropped.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)
    image_scaled.save(f'{output_base_path}_scaled.jpg')

    # 应用高斯模糊，并保存
    image_blurred = image_scaled.filter(ImageFilter.GaussianBlur(21))
    image_blurred.save(f'{output_base_path}_blurred.jpg')

    # 将原始裁剪的图片叠加到模糊的图片上，并保存
    overlay_left = (image_blurred.width - image_cropped.width) // 2
    overlay_top = (image_blurred.height - image_cropped.height) // 2
    image_blurred.paste(image_cropped, (overlay_left, overlay_top))
    image_blurred.save(f'{output_base_path}_overlay_before_final_crop.jpg')

    # 最后裁剪overlay.jpg的中心位置以匹配原始图片尺寸
    final_crop_left = (image_blurred.width - original_size[0]) // 2
    final_crop_top = (image_blurred.height - original_size[1]) // 2
    image_final = image_blurred.crop((final_crop_left, final_crop_top, final_crop_left + original_size[0], final_crop_top + original_size[1]))
    image_final.save(f'{output_base_path}_overlay.jpg')

# 使用示例
image_path = '8881.jpg'  # 请确保此路径与实际图片路径相匹配
output_base_path = 'processed_image'
crop_scale_blur_overlay_correct_position_and_final_crop(image_path, output_base_path)
