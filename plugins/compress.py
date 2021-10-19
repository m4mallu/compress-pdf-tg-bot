import os
import time
import asyncio
from presets import Presets
from pyrogram.types import Message
from pyrogram import Client, filters
from support.file_size import get_size
from PDFNetPython3.PDFNetPython import *
from support.markups import close_button
from support.display_progress import progress_for_pyrogram


@Client.on_message(filters.private & filters.document)
async def compress_pdf(c, m: Message):
    msg = await m.reply_text(Presets.WAIT_MESSAGE, reply_to_message_id=m.message_id)
    if not str(m.document.file_name).lower().endswith('.pdf'):
        await msg.edit(Presets.INVALID_FORMAT, reply_markup=close_button)
        return
    #
    dl_location = os.getcwd() + '/' + "downloads" + '/' + str(m.from_user.id) + '/'
    if not os.path.isdir(dl_location):
        os.makedirs(dl_location)
    else:
        for f in os.listdir(dl_location):
            try:
                os.remove(os.path.join(dl_location, f))
            except Exception:
                pass
    #
    await asyncio.sleep(2)
    await msg.edit(Presets.DOWNLOAD_MSG)
    current_time = time.time()
    await m.download(
        file_name=dl_location,
        progress=progress_for_pyrogram,
        progress_args=(
            Presets.DOWNLOAD_MSG,
            msg,
            current_time
        )
    )
    #
    await asyncio.sleep(1)
    await msg.edit(Presets.FINISHED_DL)
    await asyncio.sleep(2)
    await msg.edit(Presets.START_COMPRESSING)
    await asyncio.sleep(2)
    #
    # Let's find out the initial document size
    size_path = await get_size(dl_location)
    initial_size = size_path[0]
    #
    try:
        """
            I have used PDFNetPython3 package which found to be a better one to compress the pdf documents using python.
            Link: https://www.thepythoncode.com/article/compress-pdf-files-in-python
        """
        # Initialize the library
        PDFNet.Initialize()
        doc = PDFDoc(size_path[1])
        # Optimize PDF with the default settings
        doc.InitSecurityHandler()
        # Reduce PDF size by removing redundant information and compressing data streams
        Optimizer.Optimize(doc)
        doc.Save(size_path[1], SDFDoc.e_linearized)
        doc.Close()
    except Exception:
        await msg.edit(Presets.JOB_ERROR, reply_markup=close_button)
        return
    #
    # Let's find out the compressed document file size
    size_path = await get_size(dl_location)
    compressed_size = size_path[0]
    #
    await asyncio.sleep(2)
    message = await msg.edit(Presets.UPLOAD_MSG)
    current_time = time.time()
    #
    await m.reply_document(
        document=size_path[1],
        reply_to_message_id=m.message_id,
        caption=m.caption if m.caption else '',
        progress=progress_for_pyrogram,
        progress_args=(
            Presets.UPLOAD_MSG,
            message,
            current_time
        )

    )
    #
    try:
        os.remove(size_path[1])
    except Exception:
        pass
    #
    await msg.edit(Presets.FINISHED_JOB.format(initial_size, compressed_size),
                   disable_web_page_preview=True,
                   reply_markup=close_button
                   )
