import React, { useState } from 'react';
import { Box, Button, Text, VStack, useToast, Input } from '@chakra-ui/react';
import { FaImage } from 'react-icons/fa';

const ImgurUploader = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadedUrl, setUploadedUrl] = useState('');
  const toast = useToast();

  const handleFileSelect = (event) => {
    setSelectedFile(event.target.files[0]);
    setUploadedUrl('');
  };

  const uploadToImgur = async () => {
    if (!selectedFile) {
      toast({
        title: 'No file selected',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await fetch('https://api.imgur.com/3/image', {
        method: 'POST',
        headers: {
          Authorization: `Client-ID ${process.env.REACT_APP_IMGUR_CLIENT_ID}`,
        },
        body: formData,
      });

      const data = await response.json();
      
      if (data.success) {
        setUploadedUrl(data.data.link);
        toast({
          title: 'Upload successful',
          status: 'success',
          duration: 3000,
          isClosable: true,
        });
      } else {
        throw new Error('Upload failed');
      }
    } catch (error) {
      toast({
        title: 'Upload failed',
        description: error.message,
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setUploading(false);
    }
  };

  return (
    <Box p={6} borderRadius="lg" bg="white" boxShadow="md" width="100%">
      <VStack spacing={4} align="stretch">
        <Text fontSize="xl" fontWeight="bold">
          Imgur Uploader
        </Text>
        <Input
          type="file"
          accept="image/*"
          onChange={handleFileSelect}
          p={1}
        />
        <Button
          leftIcon={<FaImage />}
          colorScheme="purple"
          onClick={uploadToImgur}
          isLoading={uploading}
          loadingText="Uploading..."
        >
          Upload to Imgur
        </Button>
        {uploadedUrl && (
          <VStack spacing={2}>
            <Text>Upload successful! Here's your link:</Text>
            <Input value={uploadedUrl} isReadOnly />
          </VStack>
        )}
      </VStack>
    </Box>
  );
};

export default ImgurUploader; 