from db import db as db_con


def variants_summary(file_hash):
    query = """
    SELECT chrom, gene_hgnc, count(*) AS count
    FROM variants
    GROUP BY 1, 2
    ORDER BY 1 ASC, 3 DESC
    """
    return db_con.execute(query).fetch_df()


def effects_by_impact_summary(file_hash):
    query = """
    SELECT chrom, v.gene_hgnc, impact, effect, count(*) AS count
    FROM variants v
    JOIN annotations a ON v.file_hash = a.file_hash AND v.gene_hgnc = a.gene_hgnc AND v.gene_variation = a.gene_variation
    WHERE effect NOT IN ('intergenic_region')
    GROUP BY 1, 2, 3, 4
    ORDER BY 1 ASC, 2 ASC, 3 ASC, 5 DESC
    """
    return db_con.execute(query).fetch_df()


def transcripts_overview(file_hash):
    query = """
    SELECT chrom, v.gene_hgnc, transcript_biotype, COUNT(*) AS count
    FROM variants v
    JOIN annotations a ON v.file_hash = a.file_hash AND v.gene_hgnc = a.gene_hgnc AND v.gene_variation = a.gene_variation
    WHERE effect NOT IN ('intergenic_region')
    GROUP BY 1, 2, 3
    ORDER BY 1 ASC, 2 ASC, 4 DESC
    """
    return db_con.execute(query).fetch_df()


def impact_summary(file_hash):
    query = """
    SELECT
    chrom,
    v.gene_hgnc,
    SUM(CASE impact WHEN 'HIGH' THEN 1 ELSE 0 END) AS high_impact, 
    SUM(CASE impact WHEN 'MODERATE' THEN 1 ELSE 0 END) AS moderate_impact, 
    SUM(CASE impact WHEN 'LOW' THEN 1 ELSE 0 END) AS low_impact, 
    SUM(CASE impact WHEN 'MODIFIER' THEN 1 ELSE 0 END) AS modifiers
    FROM variants v
    JOIN annotations a ON v.file_hash = a.file_hash AND v.gene_hgnc = a.gene_hgnc AND v.gene_variation = a.gene_variation
    WHERE effect NOT IN ('intergenic_region')
    GROUP BY 1, 2
    ORDER BY 1 ASC, 2 ASC, 3 DESC, 4 DESC, 5 DESC, 6 DESC
    """
    return db_con.execute(query).fetch_df()