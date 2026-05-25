import { useEffect, useRef } from 'react'
import { Box, Flex, Heading, Stack, Text } from '@chakra-ui/react'
import { useIntl } from 'react-intl'

import { useChat } from '../../hooks/useChat'
import { MessageBubble } from './MessageBubble'
import { TypingIndicator } from './TypingIndicator'
import { messages as uiMessages } from './messages'

export function MessagesPanel() {
  const { messages, isSending } = useChat()
  const intl = useIntl()
  const endOfMessagesRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isSending])

  return (
    <Box flex="1" overflowY="auto" px={4} py={5}>
      {messages.length === 0 ? (
        <Flex
          h="full"
          minH="320px"
          align="center"
          justify="center"
          textAlign="center"
        >
          <Box maxW="lg">
            <Heading size="md">{intl.formatMessage(uiMessages.emptyTitle)}</Heading>
            <Text mt={2} color="gray.600">
              {intl.formatMessage(uiMessages.emptyDescription)}
            </Text>
          </Box>
        </Flex>
      ) : (
        <Stack gap={4}>
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
        </Stack>
      )}

      {isSending ? (
        <Box mt={4}>
          <TypingIndicator />
        </Box>
      ) : null}

      <div ref={endOfMessagesRef} />
    </Box>
  )
}
