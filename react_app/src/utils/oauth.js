export const generateCodeVerifier = () => {
    const array = new Uint32Array(56 / 2);
    crypto.getRandomValues(array);
    return Array.from(array, dec => ('0' + dec.toString(16)).substr(-2)).join('');
}

export const generateCodeChallenge = async (verifier) => {
    const encoder = new TextEncoder();
    const data = encoder.encode(verifier);
    const digest = await crypto.subtle.digest('SHA-256', data);
    return btoa(String.fromCharCode.apply(null, [...new Uint8Array(digest)]))
        .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

export const initiateGoogleAuth = async () => {
    const verifier = generateCodeVerifier();
    sessionStorage.setItem('code_verifier', verifier);
    const state = Math.random().toString(36).substring(7);
    sessionStorage.setItem('oauth_state', state);

    const challenge = await generateCodeChallenge(verifier);

    const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID || "TU_CLIENT_ID_AQUI";
    const redirectUri = "http://localhost:5173/auth/callback";

    const params = new URLSearchParams({
        client_id: clientId,
        redirect_uri: redirectUri,
        response_type: "code",
        scope: "openid profile email",
        code_challenge: challenge,
        code_challenge_method: "S256",
        state: state
    });

    window.location.href = `https://accounts.google.com/o/oauth2/v2/auth?${params.toString()}`;
}
