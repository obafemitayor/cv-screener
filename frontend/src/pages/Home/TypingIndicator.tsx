import { Box, Flex, HStack, Spinner, Text } from '@chakra-ui/react'
import { useIntl } from 'react-intl'

import { messages } from './messages'

export function TypingIndicator() {
  const intl = useIntl()

  return (
    <Flex justify="flex-start">
      <Box
        maxW="min(92%, 52rem)"
        borderRadius="2xl"
        bg="gray.100"
        color="gray.700"
        px={4}
        py={3}
        shadow="sm"
      >
        <HStack gap={3}>
          <Spinner size="sm" />
          <Text fontSize="sm">{intl.formatMessage(messages.thinking)}</Text>
        </HStack>
      </Box>
    </Flex>
  )
}
