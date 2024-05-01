export class UserObj {
  name: string;
  email: string;
  id: number;
  sub?: string;

  constructor(name: string, email: string, id: number, sub?: string) {
    this.name = name;
    this.email = email;
    this.id = id;
    this.sub = sub;
  }
}
