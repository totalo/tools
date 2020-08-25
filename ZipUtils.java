public static void zipFilePip() {

    long beginTime = System.currentTimeMillis();
    try(WritableByteChannel out = Channels.newChannel(new FileOutputStream(ZIP_FILE))) {
        Pipe pipe = Pipe.open();
        //异步任务
        CompletableFuture.runAsync(()->runTask(pipe));

        //获取读通道
        ReadableByteChannel readableByteChannel = pipe.source();
        ByteBuffer buffer = ByteBuffer.allocate(((int) FILE_SIZE)*10);
        while (readableByteChannel.read(buffer)>= 0) {
            buffer.flip();
            out.write(buffer);
            buffer.clear();
        }
    }catch (Exception e){
        e.printStackTrace();
    }
    printInfo(beginTime);

}

//异步任务
public static void runTask(Pipe pipe) {

    try(ZipOutputStream zos = new ZipOutputStream(Channels.newOutputStream(pipe.sink()));
            WritableByteChannel out = Channels.newChannel(zos)) {
        System.out.println("Begin");
        for (int i = 0; i < 10; i++) {
            zos.putNextEntry(new ZipEntry(i+SUFFIX_FILE));

            FileChannel jpgChannel = new FileInputStream(new File(JPG_FILE_PATH)).getChannel();

            jpgChannel.transferTo(0, FILE_SIZE, out);

            jpgChannel.close();
        }
    }catch (Exception e){
        e.printStackTrace();
    }
}
