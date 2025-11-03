declare module 'negotiator' {
  interface NegotiatorHeaders {
    headers: Record<string, string | string[]>;
  }

  export default class Negotiator {
    constructor(request: NegotiatorHeaders);
    languages(available?: readonly string[]): string[];
  }
}

