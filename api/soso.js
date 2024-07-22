import { join } from 'path';
import { parse } from 'url';
import { promisify } from 'util';
import { spawn } from 'child_process';

const exec = promisify(spawn);

export default async function handler(req, res) {
     try {
       const { pathname } = parse(req.url);
       const result = await exec('python', [join(__dirname, 'soso.py'), pathname]);
       const output = result.stdout.toString();
       res.status(200).json({ message: output });
     } catch (error) {
       console.error('Error executing Python script:', error);
       res.status(500).json({ error: 'Error running the script' });
     }
   }

