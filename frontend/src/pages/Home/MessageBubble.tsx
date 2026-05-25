import { Box, Flex, Text } from '@chakra-ui/react'

import type { ChatMessage as ChatMessageType } from '../../types/chat'

export function MessageBubble({ message }: { message: ChatMessageType }) {
  const isUser = message.role === 'user'

  return (
    <Flex justify={isUser ? 'flex-end' : 'flex-start'}>
      <Box
        maxW="min(92%, 52rem)"
        borderRadius="2xl"
        bg={isUser ? 'blue.600' : 'gray.100'}
        color={isUser ? 'white' : 'gray.800'}
        px={4}
        py={3}
        shadow="sm"
      >
        <Text whiteSpace="pre-wrap" lineHeight="1.65">
          {message.content}
        </Text>
      </Box>
    </Flex>
  )
}
