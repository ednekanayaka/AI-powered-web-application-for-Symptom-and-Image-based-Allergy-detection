export function decodeToken(token) {
  try {
    const base64 = token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/");
    return JSON.parse(atob(base64));
  } catch {
    return null;
  }
}

export function getTokenPayload() {
  const token = localStorage.getItem("access");
  if (!token) {
    return null;
  }
  return decodeToken(token);
}

export function isTokenExpired(payload, skewSeconds = 30) {
  if (!payload?.exp) {
    return true;
  }
  const now = Math.floor(Date.now() / 1000);
  return payload.exp <= now + skewSeconds;
}

export function clearStoredTokens() {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
}

export function getIsAdmin() {
  const payload = getTokenPayload();
  if (!payload || isTokenExpired(payload)) {
    return false;
  }
  return payload?.is_admin === true;
}
