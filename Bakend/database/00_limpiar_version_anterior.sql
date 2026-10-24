-- =====================================================================
-- Limpieza opcional: borra la primera versión (React + Supabase Auth)
-- que quedó en el esquema "public". Ejecútelo en el SQL Editor de Supabase.
-- La aplicación PHP usa el esquema "clinica" y no depende de estas tablas.
-- =====================================================================
drop table if exists public.notificacion, public.estudio, public.catalogoestudio, public.tratamiento,
    public.medicamento, public.consulta, public.historialcita, public.cita, public.estadocita,
    public.historiaclinica, public.contactoemergencia, public.paciente, public.bloqueoagenda,
    public.horario, public.medicoespecialidad, public.medico, public.especialidad,
    public.configuracion, public.bitacora, public.usuario, public.rol cascade;
drop function if exists public.mi_idusuario(), public.mi_rol(), public.es_admin(), public.ip_solicitud(),
    public.registrar_bitacora(text, text, text, integer, text), public.trg_bitacora(), public.trg_proteger_rol(),
    public.validar_datos_usuario(text, text, text, text, boolean), public._crear_usuario(text, text, text, text, integer),
    public.crear_usuario(text, text, text, text, integer), public.actualizar_usuario(integer, text, text, text, integer, text),
    public.cambiar_estado_usuario(integer), public.email_de_login(text), public.registrar_acceso(), public.registrar_salida(),
    public.cambiar_password(text, text), public.mi_perfil(), public.estadisticas_panel() cascade;
delete from auth.users where email like '%@headsalud.com' or email = 'jperez@correo.com';
