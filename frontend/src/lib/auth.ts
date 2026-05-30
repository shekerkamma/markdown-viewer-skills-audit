export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("ticketforge_token");
}

export function isAuthenticated(): boolean {
  return getToken() !== null;
}

export function logout(): void {
  localStorage.removeItem("ticketforge_token");
  window.location.href = "/";
}
