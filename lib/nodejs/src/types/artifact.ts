/**
 * Canonical artifact interface.
 * Defined in schemas/draft/artifact.schema.json
 */
export interface Artifact {
    /**
     * Type of artifact (file, diff, patch, action, message, etc). Free-form and engine-defined.
     */
    artifact_type: string;
    /**
     * Operation to perform with this artifact (create, update, delete, apply, execute, etc). Free-form and engine-defined.
     */
    action: string;
    /**
     * Path, resource, or identifier this artifact applies to. Optional.
     */
    target?: string;
    /**
     * MIME type describing content.
     */
    mime: string;
    /**
     * Inline content for small artifacts.
     * Can be string, object, array, or null.
     */
    body?: string | object | any[] | null;
    /**
     * Indicates an external data file within the artifact directory.
     */
    body_file?: string;
    /**
     * Arbitrary metadata. Optional.
     */
    metadata?: Record<string, any>;
}
