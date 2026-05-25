import { useState, type FormEvent, type KeyboardEvent } from 'react'
import { Box, Button, Flex, HStack, Stack, Text, Textarea } from '@chakra-ui/react'
import { SendHorizontal } from 'lucide-react'
import { useIntl } from 'react-intl'

import { useChat } from '../../hooks/useChat'
import { messages } from './messages'

export function QuestionInput() {
  const { error, isSending, sendQuestion } = useChat()
  const intl = useIntl()
  const [questionText, setQuestionText] = useState('')

  async function submitQuestion() {
    const trimmedQuestion = questionText.trim()
    if (!trimmedQuestion || isSending) {
      return
    }

    setQuestionText('')
    await sendQuestion(trimmedQuestion)
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    await submitQuestion()
  }

  async function handleSubmitViaEnterKey(
    event: KeyboardEvent<HTMLTextAreaElement>,
  ) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      await submitQuestion()
    }
  }

  return (
    <Box px={4} py={4}>
      {error ? (
        <Box
          mb={4}
          borderWidth="1px"
          borderColor="red.200"
          bg="red.50"
          borderRadius="xl"
          px={4}
          py={3}
          role="alert"
        >
          <Text fontSize="sm" color="red.700">
            {intl.formatMessage(messages.error)}
          </Text>
        </Box>
      ) : null}

      <form onSubmit={handleSubmit}>
        <Stack gap={3}>
          <Textarea
            value={questionText}
            onChange={(event) => setQuestionText(event.target.value)}
            onKeyDown={handleSubmitViaEnterKey}
            placeholder={intl.formatMessage(messages.placeholder)}
            minH="96px"
            resize="vertical"
            bg="white"
          />

          <Flex justify="flex-end">
            <Button
              type="submit"
              bg="blue.600"
              color="white"
              _hover={{ bg: 'blue.700' }}
              _disabled={{ opacity: 0.6, cursor: 'not-allowed' }}
              disabled={!questionText.trim() || isSending}
            >
              <HStack gap={2}>
                <SendHorizontal size={16} />
                <Text>{intl.formatMessage(messages.send)}</Text>
              </HStack>
            </Button>
          </Flex>
        </Stack>
      </form>
    </Box>
  )
}
