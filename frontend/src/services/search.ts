import type {
  ChatHistoryMessage,
  SearchRequest,
  SearchResponse,
} from '../types/chat'
import { client } from '../lib/api'

export async function queryCVs(
  query: string,
  chatHistory: ChatHistoryMessage[],
): Promise<SearchResponse> {
  const payload: SearchRequest = {
    query,
    chat_history: chatHistory,
  }

  try {
    const response = await client.post<SearchResponse>('/search', payload)
    return response.data
  } catch (error) {
    throw new Error('Request failed.', { cause: error })
  }
}
