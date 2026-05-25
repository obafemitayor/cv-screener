import { createContext } from 'react'

import type { ChatMessage } from '../types/chat'

export interface ChatContextValue {
  messages: ChatMessage[]
  isSending: boolean
  error: boolean
  sendQuestion: (question: string) => Promise<void>
}

export const ChatContext = createContext<ChatContextValue | undefined>(
  undefined,
)
