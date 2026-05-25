import {
  useCallback,
  useMemo,
  useState,
  type ReactNode,
} from 'react'

import { queryCVs } from '../services/search'
import type { ChatHistoryMessage, ChatMessage } from '../types/chat'
import { ChatContext } from './chat-context'

function createMessageId(): string {
  return crypto.randomUUID()
}

export function ChatProvider({ children }: { children: ReactNode }) {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [isSending, setIsSending] = useState(false)
  const [error, setError] = useState(false)

  const sendQuestion = useCallback(
    async (question: string) => {
      const trimmedQuestion = question.trim()
      if (!trimmedQuestion || isSending) {
        return
      }

      const chatHistory: ChatHistoryMessage[] = messages.map(
        ({ role, content }) => ({
          role,
          content,
        }),
      )

      const userMessage: ChatMessage = {
        id: createMessageId(),
        role: 'user',
        content: trimmedQuestion,
      }

      setMessages((currentMessages) => [...currentMessages, userMessage])
      setIsSending(true)
      setError(false)

      try {
        const result = await queryCVs(trimmedQuestion, chatHistory)
        if (!result.response.trim()) {
          setError(true)
          return
        }

        const assistantMessage: ChatMessage = {
          id: createMessageId(),
          role: 'assistant',
          content: result.response,
        }

        setMessages((currentMessages) => [...currentMessages, assistantMessage])
      } catch {
        setError(true)
      } finally {
        setIsSending(false)
      }
    },
    [isSending, messages],
  )

  const contextValue = useMemo(
    () => ({
      messages,
      isSending,
      error,
      sendQuestion,
    }),
    [messages, isSending, error, sendQuestion],
  )

  return (
    <ChatContext.Provider value={contextValue}>
      {children}
    </ChatContext.Provider>
  )
}
