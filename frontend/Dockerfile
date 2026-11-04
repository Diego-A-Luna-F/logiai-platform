# Usar Node.js ligero como base
FROM node:20-alpine

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto del código del frontend
COPY . .

# Exponer el puerto de Vite
EXPOSE 5173

# Comando para iniciar en modo desarrollo exponiendo la red al contenedor
CMD ["npm", "run", "dev", "--", "--host"]