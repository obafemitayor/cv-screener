import { Box, Container, Heading, Separator, Stack, Text } from '@chakra-ui/react'
import { useIntl } from 'react-intl'

import { messages as uiMessages } from './messages'
import { MessagesPanel } from './MessagesPanel'
import { QuestionInput } from './QuestionInput'

export function Home() {
  const intl = useIntl()

  return (
    <Box minH="100dvh" bg="gray.50" py={{ base: 4, md: 8 }}>
      <Container maxW="5xl">
        <Stack gap={4}>
          <Box textAlign="center">
            <Heading size="lg">{intl.formatMessage(uiMessages.appTitle)}</Heading>
            <Text mt={2} color="gray.600">
              {intl.formatMessage(uiMessages.appDescription)}
            </Text>
          </Box>

          <Box
            display="flex"
            minH={{ base: '72dvh', md: '78dvh' }}
            flexDirection="column"
            overflow="hidden"
            borderWidth="1px"
            borderColor="gray.200"
            borderRadius="3xl"
            bg="white"
            shadow="sm"
          >
            <MessagesPanel />

            <Separator />

            <QuestionInput />
          </Box>
        </Stack>
      </Container>
    </Box>
  )
}
