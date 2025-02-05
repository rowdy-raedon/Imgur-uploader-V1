import ImgurUploader from './components/ImgurUploader';

function App() {
  return (
    <ChakraProvider>
      <Box minH="100vh" bg="gray.100">
        <Container maxW="container.xl" py={8}>
          <VStack spacing={6}>
            <ImgurUploader />
          </VStack>
        </Container>
      </Box>
    </ChakraProvider>
  );
}

export default App; 