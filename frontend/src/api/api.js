// frontend/src/api/api.js
// Lightweight fetch-based API helper

const BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api';

function buildUrl(path, params) {
    const normalized = path.startsWith('/') ? path : `/${path}`;
    const url = new URL(BASE_URL + normalized);
    if (params && typeof params === 'object') {
        Object.entries(params).forEach(([k, v]) => {
            if (v !== undefined && v !== null) url.searchParams.append(k, v);
        });
    }
    return url.toString();
}

function getAuthHeaders() {
    const token = localStorage.getItem('token') || null;
    const headers = {};
    if (token) headers.Authorization = `Bearer ${token}`;
    return headers;
}

async function handleResponse(response) {
    const contentType = response.headers.get('content-type') || '';
    const isJson = contentType.includes('application/json');
    const body = isJson ? await response.json().catch(() => null) : await response.text().catch(() => null);

    if (response.ok) {
        return body === '' ? null : body;
    }

    const err = new Error((body && (body.message || body.error)) || response.statusText || 'API error');
    err.status = response.status;
    err.body = body;
    throw err;
}

async function request(method, path, { params, body, headers = {}, signal } = {}) {
    const url = buildUrl(path, params);
    const authHeaders = getAuthHeaders();
    const opts = {
        method,
        headers: { ...authHeaders, ...headers },
        signal,
    };

    if (body !== undefined && body !== null) {
        if (body instanceof FormData) {
            // Let fetch set the correct Content-Type for FormData
            opts.body = body;
        } else {
            opts.headers['Content-Type'] = 'application/json';
            opts.body = JSON.stringify(body);
        }
    }

    const res = await fetch(url, opts);
    return handleResponse(res);
}

// exported convenience functions
export function get(path, params, opts = {}) {
    return request('GET', path, { params, ...opts });
}

export function post(path, body, opts = {}) {
    return request('POST', path, { body, ...opts });
}

export function put(path, body, opts = {}) {
    return request('PUT', path, { body, ...opts });
}

export function del(path, body, opts = {}) {
    return request('DELETE', path, { body, ...opts });
}

export function upload(path, formData, opts = {}) {
    return request('POST', path, { body: formData, ...opts });
}

export default {
    get,
    post,
    put,
    delete: del,
    upload,
};