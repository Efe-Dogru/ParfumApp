export const useBucketImages = async (bucketName: string, filePath: string) => {
  const client = useSupabaseClient();

  // Get the public URL for the file
  const { data } = client.storage.from(bucketName).getPublicUrl(filePath);
    return data.publicUrl;
};
