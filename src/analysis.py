import db


def variants_summary(file_hash):
    query = """
    SELECT chrom, gene_hgnc, count(*) AS count
    FROM variants
    WHERE file_hash = ?
    GROUP BY 1, 2
    ORDER BY 1 ASC, 3 DESC
    """
    return db.read_query(query, (file_hash,))


def effects_by_impact_summary_for_gene(file_hash, gene_hgnc, biotypes=None):
    if biotypes:
        query = """
        SELECT impact, effect, count(*) AS count
        FROM variants v
        JOIN annotations a ON v.file_hash = a.file_hash AND v.gene_hgnc = a.gene_hgnc AND v.gene_variation = a.gene_variation
        WHERE v.file_hash = ?
          AND a.gene_hgnc = ?
          AND effect NOT IN ('intergenic_region')
          AND transcript_biotype IN ({biotypes})
        GROUP BY 1, 2
        ORDER BY 1 ASC, 3 DESC
        """.format(biotypes=','.join(['?'] * len(biotypes)))
        return db.read_query(query, [file_hash, gene_hgnc] + biotypes)
    else:
        query = """
        SELECT impact, effect, count(*) AS count
        FROM variants v
        JOIN annotations a ON v.file_hash = a.file_hash AND v.gene_hgnc = a.gene_hgnc AND v.gene_variation = a.gene_variation
        WHERE v.file_hash = ?
          AND a.gene_hgnc = ?
          AND effect NOT IN ('intergenic_region')
        GROUP BY 1, 2
        ORDER BY 1 ASC, 3 DESC
        """
        return db.read_query(query, (file_hash, gene_hgnc))


def transcripts_overview(file_hash):
    query = """
    SELECT chrom, v.gene_hgnc, transcript_biotype, COUNT(*) AS count
    FROM variants v
    JOIN annotations a ON v.file_hash = a.file_hash AND v.gene_hgnc = a.gene_hgnc AND v.gene_variation = a.gene_variation
    WHERE v.file_hash = ? AND effect NOT IN ('intergenic_region')
    GROUP BY 1, 2, 3
    ORDER BY 1 ASC, 2 ASC, 4 DESC
    """
    return db.read_query(query, (file_hash,))


def impact_summary(file_hash):
    query = """
    SELECT
    chrom,
    v.gene_hgnc,
    COUNT(DISTINCT v.gene_variation) AS variants,
    SUM(CASE impact WHEN 'HIGH' THEN 1 ELSE 0 END) AS high_impact, 
    SUM(CASE impact WHEN 'MODERATE' THEN 1 ELSE 0 END) AS moderate_impact, 
    SUM(CASE impact WHEN 'LOW' THEN 1 ELSE 0 END) AS low_impact, 
    SUM(CASE impact WHEN 'MODIFIER' THEN 1 ELSE 0 END) AS modifiers
    FROM variants v
    JOIN annotations a ON v.file_hash = a.file_hash AND v.gene_hgnc = a.gene_hgnc AND v.gene_variation = a.gene_variation
    WHERE v.file_hash = ? AND effect NOT IN ('intergenic_region')
    GROUP BY 1, 2
    ORDER BY 1 ASC, 2 ASC, 3 DESC, 4 DESC, 5 DESC, 6 DESC
    """
    return db.read_query(query, (file_hash,))


def file_summary(file_hash):
    query = """
    SELECT 
        COUNT(DISTINCT gene_hgnc) AS genes,
        COUNT(DISTINCT {g: gene_hgnc, v: gene_variation}) AS variations,
        COUNT(*) AS effects
    FROM annotations
    WHERE file_hash = ?
      AND effect NOT IN ('intergenic_region')
    """
    return db.read_query(query, (file_hash,))


def get_transcript_biotypes(file_hash, gene_hgnc):
    query = """
    SELECT DISTINCT transcript_biotype
    FROM annotations
    WHERE file_hash = ?
      AND gene_hgnc = ?
      AND effect NOT IN ('intergenic_region')
    """
    return db.read_query(query, (file_hash, gene_hgnc))['transcript_biotype'].tolist()


def get_effects(file_hash, gene_hgnc):
    query = """
    SELECT DISTINCT effect
    FROM annotations
    WHERE file_hash = ?
      AND gene_hgnc = ?
      AND effect NOT IN ('intergenic_region')
    """
    return db.read_query(query, (file_hash, gene_hgnc))['effect'].tolist()


def get_impacts(file_hash, gene_hgnc):
    query = """
    SELECT DISTINCT impact
    FROM annotations
    WHERE file_hash = ?
      AND gene_hgnc = ?
      AND effect NOT IN ('intergenic_region')
    """
    return db.read_query(query, (file_hash, gene_hgnc))['impact'].tolist()


def get_feature_types(file_hash, gene_hgnc):
    query = """
    SELECT DISTINCT feature_type
    FROM annotations
    WHERE file_hash = ?
      AND gene_hgnc = ?
      AND effect NOT IN ('intergenic_region')
    """
    return db.read_query(query, (file_hash, gene_hgnc))['feature_type'].tolist()
