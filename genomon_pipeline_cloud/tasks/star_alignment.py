#! /usr/bin/env python

import genomon_pipeline_cloud.abstract_task as abstract_task

class Star_alignment(abstract_task.Abstract_task):

    task_name = "star-alignment"

    def __init__(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        super(Star_alignment, self).__init__(
            self.__class__.task_name,
            param_conf.get("star_alignment", "image"),
            param_conf.get("star_alignment", "resource"),
            output_dir + "/logging")

        self.task_file = self.task_file_generation(output_dir, task_dir, sample_conf, param_conf, run_conf)


    def task_file_generation(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        # generate star_alignment_tasks.tsv
        #task_file = "{}/{}-tasks.tsv".format(task_dir, self.__class__.task_name)
        task_file = "{}/{}-tasks-{}-{}.tsv".format(task_dir, self.__class__.task_name, run_conf.get_owner_info(), run_conf.analysis_timestamp)
        with open(task_file, 'w') as hout:

            hout.write('\t'.join(["--env SAMPLE",
                                  "--input INPUT_BAM",
                                  "--input FASTQ1",
                                  "--input FASTQ2",
                                  "--output-recursive OUTPUT_DIR",
                                  "--input-recursive REFERENCE",
                                  "--env BAMTOFASTQ_OPTION",
                                  "--env STAR_OPTION",
                                  "--env SAMTOOLS_SORT_OPTION"]) 
                                  + "\n")

            for sample in sample_conf.fastq:
                hout.write('\t'.join([sample,
                                          '',
                                          sample_conf.fastq[sample][0][0],
                                          sample_conf.fastq[sample][1][0],
                                          output_dir + "/star/" + sample,
                                          param_conf.get("star_alignment", "star_reference"),
                                          '',
                                          param_conf.get("star_alignment", "star_option"),
                                          param_conf.get("star_alignment", "samtools_sort_option")]) + "\n")

            for sample in sample_conf.bam_tofastq:
                hout.write('\t'.join([sample,
                                      sample_conf.bam_tofastq[sample],
                                      '',
                                      '',
                                      output_dir + "/star/" + sample,
                                      param_conf.get("star_alignment", "star_reference"),
                                      param_conf.get("star_alignment", "bamtofastq_option"),
                                      param_conf.get("star_alignment", "star_option"),
                                      param_conf.get("star_alignment", "samtools_sort_option")]) 
                                      + "\n")

        return task_file
