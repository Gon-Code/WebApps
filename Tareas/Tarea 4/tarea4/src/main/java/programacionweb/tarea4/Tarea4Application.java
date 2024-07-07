package programacionweb.tarea4;


import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import programacionweb.tarea4.services.ComentarioService;
import programacionweb.tarea4.services.FotoService;

@SpringBootApplication
@Controller
public class Tarea4Application {

    @Autowired
    private FotoService fotoService;
    @Autowired
    private ComentarioService comentarioService;

    private static final int PAGE_SIZE = 20;

    public static void main(String[] args) {
        SpringApplication.run(Tarea4Application.class, args);
    }

    // La primera vista ya esta CASI completamente funcional
    // Falta que el numero en el circulo corresponda a los comentarios que tiene esa foto
    // RECORDAR eliminar la lista fotos que era de prueba
    @GetMapping("/ver-fotos-productos/{page}")
    public String verFotosProductos(@PathVariable Integer page,Model model) {
        // Manejar los botones
        Integer offset = (page - 1) * PAGE_SIZE;
        // Obtener la cantidad total de fotos
        long totalFotos = fotoService.contarTotalFotos();
        // Calcular total de paginas
        int totalPages = (int) Math.ceil((double) totalFotos / PAGE_SIZE);
        boolean tienePaginaAnterior = page > 1;
        boolean tienePaginaSiguiente = page < totalPages;
        // Obtener las ultimas 20 fotos de la db
        List<Integer> IdsArchivos = fotoService.obtenerIdPaginados(offset, PAGE_SIZE);
        // Obtener cantidad de comentarios por foto
        List<FotoConComentariosDTO> fotosConComentarios = new ArrayList<>();

    for (Integer id : IdsArchivos) {
        String nombreArchivo = fotoService.obtenerNombreArchivoPorId(id);
        Long cantidadComentarios = comentarioService.countComentariosByIdFoto(id);
        fotosConComentarios.add(new FotoConComentariosDTO(nombreArchivo, cantidadComentarios,id));
    }
        // Pasamos la lista de fotos al modelo
        model.addAttribute("fotosConComentarios", fotosConComentarios);
        model.addAttribute("currentPage", page);
        model.addAttribute("totalPages", totalPages);
        model.addAttribute("tienePaginaAnterior", tienePaginaAnterior);
        model.addAttribute("tienePaginaSiguiente", tienePaginaSiguiente);
        return "ver-fotos-productos"; // Esto hace referencia a ver-fotos-productos.html en /templates
    }

    // Método para ver una foto en específico
    // Falta realizar los STEPS de la pizarra
    @GetMapping("/ver-foto/{id}")
    public String verFoto(@PathVariable Integer id,Model model) {

        // Obtener producto_id de la foto
        Integer productoId =  fotoService.obtenerProductoIdPorIdFoto(id);
        // Obtener nombre de la foto
        String name = fotoService.obtenerNombreArchivoPorId(id);
        // Obtener id de los comentarios que tengan el parametro foto_id igual al id de la foto
        List<Integer> idsComentarios = comentarioService.findIdsByIdFoto(id);

        // Lista para almacenar los detalles de los comentarios como tuplas
        List<Triplet<String, String, LocalDateTime>> comentariosDetalles = new ArrayList<>();
        
        // Iterar sobre los ids de los comentarios
        for (Integer idComentario : idsComentarios) {
            // Obtener nombre, comentario y fecha
            String nombre = comentarioService.findNombreById(idComentario);
            String comentario = comentarioService.findComentarioById(idComentario);
            LocalDateTime fecha = comentarioService.findFechaById(idComentario);

            // Crear tupla y agregar a la lista
            Triplet<String, String, LocalDateTime> triplet = new Triplet<>(nombre, comentario, fecha);
            comentariosDetalles.add(triplet);
        }
        
        // Pasar los datos al modelo
        model.addAttribute("comentariosDetalles", comentariosDetalles); // Lista de tuplas (nombre, comentario, fecha)
        model.addAttribute("filename", name); // Nombre de la imagen
        model.addAttribute("id", id); // Id de la imagen
        model.addAttribute("productoId", productoId); 
        return "ver-foto"; // Esto hace referencia a ver-fotos-productos.html en /templates
    }

    @PostMapping("/ver-foto/{id}/add-comment")
    @ResponseBody
    public ResponseEntity<String> addComment(
        @PathVariable Integer id,
        @RequestParam String nombre,
        @RequestParam String comentario){

        // Validación de datos
        if (nombre.length() < 3 || nombre.length() > 80) {
            return ResponseEntity.badRequest().body("El nombre debe tener entre 3 y 80 caracteres.");
        }
        if (comentario.length() < 3 || comentario.length() > 200) {
            return ResponseEntity.badRequest().body("El comentario debe tener entre 3 y 200 caracteres.");
        }
        //Obtener producto_id de la foto
        Integer productoId = fotoService.obtenerProductoIdPorIdFoto(id);
        // Guardar el comentario en la base de datos

        LocalDateTime fecha = LocalDateTime.now();
        comentarioService.guardarComentario(id, nombre, comentario, fecha, productoId);

        return ResponseEntity.ok().body("Comentario agregado exitosamente");
    }



}
