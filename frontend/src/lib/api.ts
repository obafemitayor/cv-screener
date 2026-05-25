import axios from 'axios'

import { VITE_API_BASE_URL } from '../env'

export const client = axios.create({
  baseURL: VITE_API_BASE_URL || 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})
