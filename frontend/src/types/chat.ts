export type ChatRole = 'user' | 'assistant'

export interface ChatHistoryMessage {
  role: ChatRole
  content: string
}

export interface ChatMessage extends ChatHistoryMessage {
  id: string
}

export interface SearchRequest {
  query: string
  chat_history: ChatHistoryMessage[]
}

export interface SearchResponse {
  response: string
}
