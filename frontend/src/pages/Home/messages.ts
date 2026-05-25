import { defineMessages } from 'react-intl'

export const messages = defineMessages({
  error: {
    id: 'chat.error',
    defaultMessage: 'Request failed.',
  },
  appTitle: {
    id: 'app.title',
    defaultMessage: 'CV Screening Application',
  },
  appDescription: {
    id: 'app.description',
    defaultMessage:
      'This application helps you screen out applicants from the resume pool.',
  },
  emptyTitle: {
    id: 'chat.emptyTitle',
    defaultMessage: 'Start with a question',
  },
  emptyDescription: {
    id: 'chat.emptyDescription',
    defaultMessage:
      'Try asking who has Python experience, who knows MySQL, or any other question about the CV collection.',
  },
  placeholder: {
    id: 'chat.placeholder',
    defaultMessage: 'Type your question...',
  },
  send: {
    id: 'chat.send',
    defaultMessage: 'Send',
  },
  thinking: {
    id: 'chat.thinking',
    defaultMessage: 'Thinking...',
  },
})
