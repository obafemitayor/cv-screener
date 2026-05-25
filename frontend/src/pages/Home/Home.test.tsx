import { beforeEach, describe, expect, it, jest } from '@jest/globals'
import '@testing-library/jest-dom/jest-globals'

import { ChakraProvider, defaultSystem } from '@chakra-ui/react'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

import { ChatProvider } from '../../context/ChatProvider'
import { queryCVs } from '../../services/search'
import { Home } from './index'

jest.mock('../../services/search', () => ({
  queryCVs: jest.fn(),
}))

jest.mock('react-intl', () => ({
  defineMessages: (messages: unknown) => messages,
  useIntl: () => ({
    formatMessage: ({ defaultMessage }: { defaultMessage?: string }) =>
      defaultMessage ?? '',
  }),
}))

jest.mock('lucide-react', () => ({
  SendHorizontal: () => null,
}))

const mockedQueryCVs = jest.mocked(queryCVs)

function renderHome() {
  return render(
    <ChakraProvider value={defaultSystem}>
      <ChatProvider>
        <Home />
      </ChatProvider>
    </ChakraProvider>,
  )
}

describe('Home', () => {
  beforeEach(() => {
    mockedQueryCVs.mockReset()
  })

  it('shows an error state when the api returns no response for a question', async () => {
    const user = userEvent.setup()
    mockedQueryCVs.mockResolvedValueOnce({ response: '' })

    renderHome()

    await user.type(
      screen.getByPlaceholderText('Type your question...'),
      'Who has Python experience?',
    )
    await user.click(screen.getByRole('button', { name: 'Send' }))

    expect(
      await screen.findByText('Who has Python experience?'),
    ).toBeInTheDocument()
    expect(await screen.findByRole('alert')).toHaveTextContent('Request failed.')
    expect(mockedQueryCVs).toHaveBeenCalledTimes(1)
  })

  it('displays text in the chat panel when api returns a response', async () => {
    const user = userEvent.setup()
    mockedQueryCVs.mockResolvedValueOnce({
      response: 'Jane Doe has Python experience.',
    })

    renderHome()

    await user.type(
      screen.getByPlaceholderText('Type your question...'),
      'Who has Python experience?',
    )
    await user.click(screen.getByRole('button', { name: 'Send' }))

    expect(
      await screen.findByText('Who has Python experience?'),
    ).toBeInTheDocument()
    expect(
      await screen.findByText('Jane Doe has Python experience.'),
    ).toBeInTheDocument()
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
    expect(mockedQueryCVs).toHaveBeenCalledTimes(1)
  })
})
