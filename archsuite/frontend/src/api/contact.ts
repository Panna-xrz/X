import request from './request'
import type { ContactPerson, ContactType, PageResult } from '@/types'

function unwrap<T>(p: Promise<any>): Promise<T> {
  return p.then((res: any) => res as unknown as T)
}

export type ContactPayload = Partial<Pick<ContactPerson, 'contactType' | 'name' | 'role' | 'phone' | 'remarks'>>

export function getContacts(params: {
  projectId: number
  contactType?: ContactType
  page?: number
  pageSize?: number
}): Promise<PageResult<ContactPerson>> {
  return unwrap(request.get('/contacts', { params }))
}

export function createContact(payload: ContactPayload & { name: string; projectId: number; contactType?: ContactType }): Promise<ContactPerson> {
  return unwrap(request.post('/contacts', payload))
}

export function getContact(id: number): Promise<ContactPerson> {
  return unwrap(request.get(`/contacts/${id}`))
}

export function updateContact(id: number, payload: ContactPayload): Promise<ContactPerson> {
  return unwrap(request.put(`/contacts/${id}`, payload))
}

export function deleteContact(id: number): Promise<void> {
  return unwrap(request.delete(`/contacts/${id}`))
}
