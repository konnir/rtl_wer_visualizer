import jiwer
from service.custom.allowed_replacements_handler import AllowedReplacementsHandler

class RtlCheckerService:

    def __init__(self) -> None:
        self._allowed_replacements = AllowedReplacementsHandler()
    def check_rtl_text(self, ref: str, hyp: str) -> str:

        ref = self._allowed_replacements.apply_allowed_replacements(ref)
        hyp = self._allowed_replacements.apply_allowed_replacements(hyp)

        report = jiwer.process_words(ref, hyp)

        hyp = hyp.translate(str.maketrans('', '', '<>[](){}'))
        ref = ref.translate(str.maketrans('', '', '<>[](){}'))

        splitted_stt_output = hyp.split()
        splitted_reference = ref.split()
        encoded_text = []

        for item in report.alignments[0]:
            if item.type == 'equal':
                for index in range(item.hyp_start_idx, item.hyp_end_idx):
                    encoded_text.append(splitted_stt_output[index])
            elif item.type == 'insert':
                insert = []
                for index in range(item.hyp_start_idx, item.hyp_end_idx):
                    insert.append(splitted_stt_output[index])
                    insert_str = ' '.join(insert)
                encoded_text.append(f"{{{insert_str}}}")
            elif item.type == 'delete':
                for index in range(item.ref_start_idx, item.ref_end_idx):
                    encoded_text.append(f"[{splitted_reference[index]}]")
            elif item.type == 'substitute':
                original = [splitted_stt_output[i] for i in range(item.hyp_start_idx, item.hyp_end_idx)]
                substitute = [splitted_reference[i] for i in range(item.ref_start_idx, item.ref_end_idx)]
                for i in range(len(original)):
                    encoded_text.append(f"<{original[i]}> ({substitute[i]})")
        return_text = ' '.join(encoded_text)

        report_text = (
                  f"WER: {report.wer * 100:.2f}%\n"
                  f"Substitutions: {report.substitutions}\n"
                  f"Deletions: {report.deletions}\n"
                  f"Insertions: {report.insertions}\n"
                  f"hyp Words count: {len(hyp)}\n"
                  f"ref Words count: {len(ref)}"
                )

        return return_text + "\n\n" + report_text
