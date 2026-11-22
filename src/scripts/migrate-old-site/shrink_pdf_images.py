"""Downsample large images in a PDF in place, leaving text and fonts untouched."""
import io, sys
import pikepdf
from PIL import Image

src, dst, max_side = sys.argv[1], sys.argv[2], int(sys.argv[3])
pdf = pikepdf.open(src)
done = set()
for page in pdf.pages:
    for name, raw in page.images.items():  # noqa: Page.images is deprecated but fine here
        if raw.objgen in done:
            continue
        done.add(raw.objgen)
        img = pikepdf.PdfImage(raw)
        if max(img.width, img.height) <= max_side:
            continue
        pil = img.as_pil_image()
        scale = max_side / max(pil.size)
        size = (round(pil.width * scale), round(pil.height * scale))
        pil = pil.convert("RGB").resize(size, Image.LANCZOS)
        buf = io.BytesIO(); pil.save(buf, "JPEG", quality=85, optimize=True)
        raw.write(buf.getvalue(), filter=pikepdf.Name.DCTDecode)
        raw.Width, raw.Height = size
        raw.ColorSpace = pikepdf.Name.DeviceRGB
        raw.BitsPerComponent = 8
        for key in ("/DecodeParms", "/Decode"):
            if key in raw: del raw[key]
        if "/SMask" in raw:
            mask = pikepdf.PdfImage(raw.SMask).as_pil_image().convert("L").resize(size, Image.LANCZOS)
            mbuf = mask.tobytes()
            import zlib
            raw.SMask.write(zlib.compress(mbuf), filter=pikepdf.Name.FlateDecode)
            raw.SMask.Width, raw.SMask.Height = size
            for key in ("/DecodeParms", "/Decode"):
                if key in raw.SMask: del raw.SMask[key]
        print(f"{name}: resized to {size[0]}x{size[1]}")
pdf.save(dst, compress_streams=True)
