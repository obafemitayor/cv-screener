import '@testing-library/jest-dom'

HTMLElement.prototype.scrollIntoView = jest.fn()

if (typeof globalThis.structuredClone !== 'function') {
  globalThis.structuredClone = ((value: unknown): unknown => {
    if (value === null || typeof value !== 'object') {
      return value
    }

    if (Array.isArray(value)) {
      return value.map((item) => globalThis.structuredClone(item))
    }

    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>).map(([key, entry]) => [
        key,
        globalThis.structuredClone(entry),
      ]),
    )
  }) as typeof structuredClone
}
