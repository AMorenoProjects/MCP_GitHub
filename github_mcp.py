import os
from github import Github
from dotenv import load_dotenv

class GitHubMCP:
    def __init__(self):
        """
        Inicializa el MCP de GitHub
        """
        # Cargar variables de entorno
        load_dotenv()
        
        # Obtener token de GitHub
        self.token = os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("Token de GitHub no encontrado. Por favor, configura GITHUB_TOKEN en el archivo .env")
        
        # Inicializar cliente de GitHub
        self.github = Github(self.token)
        self.user = self.github.get_user()
        
    def list_repositories(self):
        """
        Lista todos los repositorios del usuario
        """
        try:
            repos = self.user.get_repos()
            return {
                "status": "success",
                "repositories": [{
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "description": repo.description,
                    "url": repo.html_url
                } for repo in repos]
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error al listar repositorios: {str(e)}"
            }
    
    def create_branch(self, branch_name, repo_name=None):
        """
        Crea una nueva rama en el repositorio especificado
        
        Args:
            branch_name (str): Nombre de la nueva rama
            repo_name (str, optional): Nombre del repositorio. Si no se especifica, usa el repositorio actual
        """
        try:
            if repo_name:
                repo = self.github.get_repo(repo_name)
            else:
                # Asumimos que estamos en un repositorio git
                repo = self.github.get_repo(self.user.login + "/" + os.path.basename(os.getcwd()))
            
            # Obtener la rama principal
            main_branch = repo.default_branch
            
            # Crear la nueva rama
            source = repo.get_branch(main_branch)
            repo.create_git_ref(f"refs/heads/{branch_name}", source.commit.sha)
            
            return {
                "status": "success",
                "message": f"Rama '{branch_name}' creada exitosamente",
                "branch": branch_name
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error al crear la rama: {str(e)}"
            }
    
    def create_pull_request(self, title, body, head_branch, base_branch="main", repo_name=None):
        """
        Crea un nuevo Pull Request
        
        Args:
            title (str): Título del Pull Request
            body (str): Descripción del Pull Request
            head_branch (str): Rama desde la que se crea el PR
            base_branch (str): Rama base (por defecto 'main')
            repo_name (str, optional): Nombre del repositorio
        """
        try:
            if repo_name:
                repo = self.github.get_repo(repo_name)
            else:
                repo = self.github.get_repo(self.user.login + "/" + os.path.basename(os.getcwd()))
            
            # Crear el Pull Request
            pr = repo.create_pull(
                title=title,
                body=body,
                head=head_branch,
                base=base_branch
            )
            
            return {
                "status": "success",
                "message": f"Pull Request creado exitosamente",
                "pr_number": pr.number,
                "pr_url": pr.html_url
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error al crear el Pull Request: {str(e)}"
            }
    
    def search_code(self, query, language=None):
        """
        Busca código en GitHub
        
        Args:
            query (str): Término de búsqueda
            language (str, optional): Filtrar por lenguaje de programación
        """
        try:
            # Construir la consulta
            search_query = query
            if language:
                search_query += f" language:{language}"
            
            # Realizar la búsqueda
            results = self.github.search_code(search_query)
            
            # Procesar resultados
            code_results = []
            for result in results[:5]:  # Limitamos a 5 resultados
                code_results.append({
                    "name": result.name,
                    "path": result.path,
                    "repository": result.repository.full_name,
                    "url": result.html_url
                })
            
            return {
                "status": "success",
                "results": code_results
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error al buscar código: {str(e)}"
            }

def print_menu():
    """
    Muestra el menú principal
    """
    print("\n=== MCP GitHub ===")
    print("1. Listar mis repositorios")
    print("2. Crear una nueva rama")
    print("3. Crear un Pull Request")
    print("4. Buscar código")
    print("5. Salir")
    print("================")

def main():
    """
    Función principal con menú interactivo
    """
    try:
        # Crear una instancia del MCP
        github = GitHubMCP()
        
        while True:
            print_menu()
            opcion = input("\nSelecciona una opción (1-5): ")
            
            if opcion == "1":
                print("\nListando tus repositorios...")
                result = github.list_repositories()
                if result["status"] == "success":
                    print("\nTus repositorios:")
                    for repo in result["repositories"]:
                        print(f"- {repo['name']}: {repo['description']}")
                        print(f"  URL: {repo['url']}")
                else:
                    print(f"Error: {result['message']}")
            
            elif opcion == "2":
                repo_name = input("Ingresa el nombre del repositorio (usuario/repositorio): ")
                branch_name = input("Ingresa el nombre de la nueva rama: ")
                result = github.create_branch(branch_name, repo_name)
                print(f"Resultado: {result['message']}")
            
            elif opcion == "3":
                repo_name = input("Ingresa el nombre del repositorio (usuario/repositorio): ")
                title = input("Ingresa el título del Pull Request: ")
                body = input("Ingresa la descripción del Pull Request: ")
                head_branch = input("Ingresa el nombre de la rama origen: ")
                result = github.create_pull_request(title, body, head_branch, repo_name=repo_name)
                print(f"Resultado: {result['message']}")
                if result["status"] == "success":
                    print(f"URL del Pull Request: {result['pr_url']}")
            
            elif opcion == "4":
                query = input("Ingresa el término de búsqueda: ")
                language = input("Ingresa el lenguaje de programación (opcional, presiona Enter para omitir): ")
                result = github.search_code(query, language if language else None)
                if result["status"] == "success":
                    print("\nResultados encontrados:")
                    for result in result["results"]:
                        print(f"- {result['name']} en {result['repository']}")
                        print(f"  URL: {result['url']}")
                else:
                    print(f"Error: {result['message']}")
            
            elif opcion == "5":
                print("\n¡Hasta luego!")
                break
            
            else:
                print("\nOpción no válida. Por favor, selecciona una opción del 1 al 5.")
            
            input("\nPresiona Enter para continuar...")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 