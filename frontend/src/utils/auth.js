export function decodeToken(token) {
  try {
    const base64 = token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/");
    return JSON.parse(atob(base64));
  } catch {
    return null;
  }
}

export function getIsAdmin() {
  const token = localStorage.getItem("access");

  if (!token) {
    return false;
  }

  const payload = decodeToken(token);
  return payload?.is_admin === true;
}
