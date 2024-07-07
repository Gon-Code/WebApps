package programacionweb.tarea4;

public class FotoConComentariosDTO {
    private String nombreArchivo;
    private Long cantidadComentarios;
    private Integer idFoto; // Nuevo campo para el ID de la foto

    // Constructor
    public FotoConComentariosDTO(String nombreArchivo, Long cantidadComentarios, Integer idFoto) {
        this.nombreArchivo = nombreArchivo;
        this.cantidadComentarios = cantidadComentarios;
        this.idFoto = idFoto;
    }

    // Getters y setters
    public String getNombreArchivo() {
        return nombreArchivo;
    }

    public void setNombreArchivo(String nombreArchivo) {
        this.nombreArchivo = nombreArchivo;
    }

    public Long getCantidadComentarios() {
        return cantidadComentarios;
    }

    public void setCantidadComentarios(Long cantidadComentarios) {
        this.cantidadComentarios = cantidadComentarios;
    }

    public Integer getIdFoto() {
        return idFoto;
    }

    public void setIdFoto(Integer idFoto) {
        this.idFoto = idFoto;
    }
}
