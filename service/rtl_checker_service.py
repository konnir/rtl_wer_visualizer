import jiwer
from service.custom.allowed_replacements_handler import AllowedReplacementsHandler
from typing import List

class RtlCheckerService:

    def __init__(self) -> None:
        self._allowed_replacements = AllowedReplacementsHandler()

    def check_rtl_text(self, ref: str, hyp: str) -> str:

        ref = self._allowed_replacements.apply_allowed_replacements(ref)
        hyp = self._allowed_replacements.apply_allowed_replacements(hyp)

        # Keep line start tracking
        original_line_break_indices = self._get_line_break_indices(hyp)

        report = jiwer.process_words(ref, hyp)

        hyp = hyp.translate(str.maketrans('', '', '<>[](){}'))
        ref = ref.translate(str.maketrans('', '', '<>[](){}'))

        encoded_text = self._encode_text(report, ref, hyp)

        encoded_text_with_line_break = self._apply_line_breaks_with_encoding(encoded_text, original_line_break_indices)
        return_text = ' '.join(encoded_text_with_line_break)

        report_text = (
                  f"WER: {report.wer * 100:.2f}%\n"
                  f"Substitutions: {report.substitutions}\n"
                  f"Deletions: {report.deletions}\n"
                  f"Insertions: {report.insertions}\n"
                  f"hyp Words count: {len(hyp)}\n"
                  f"ref Words count: {len(ref)}"
                )

        return return_text + "\n\n" + report_text

    def _encode_text(self, report, ref: str, hyp: str):
        split_stt_output = hyp.split()
        split_reference = ref.split()
        encoded_text = []
        for item in report.alignments[0]:
            if item.type == 'equal':
                for index in range(item.hyp_start_idx, item.hyp_end_idx):
                    encoded_text.append(split_stt_output[index])
            elif item.type == 'insert':
                for index in range(item.hyp_start_idx, item.hyp_end_idx):
                    encoded_text.append(f"{{{split_stt_output[index]}}}")
            elif item.type == 'delete':
                for index in range(item.ref_start_idx, item.ref_end_idx):
                    encoded_text.append(f"[{split_reference[index]}]")
            elif item.type == 'substitute':
                original = [split_stt_output[i] for i in range(item.hyp_start_idx, item.hyp_end_idx)]
                substitute = [split_reference[i] for i in range(item.ref_start_idx, item.ref_end_idx)]
                for i in range(len(original)):
                    encoded_text.append(f"<{original[i]}>")
                    encoded_text.append(f"({substitute[i]})")
        return encoded_text

    def _get_line_break_indices(self, text: str) -> list:
        """Helper method to capture the line break indices in the original hypothesis text."""
        line_break_indices = []
        current_index = 0
        for line in text.split('\n'):
            line_break_indices.append(current_index)
            current_index += (len(line.split()))  # Track the word count at each line break
        return line_break_indices

    def _apply_line_breaks_with_encoding(self, encoded_text, original_line_break_indices):
        """Helper method to apply line breaks to the encoded text."""
        encoded_text_with_line_breaks = []
        index = 0
        for word in encoded_text:
            encoded_text_with_line_breaks.append(word)
            # insert or fix
            if word.startswith('[') or word.startswith('<'):
                continue
            else:
                index += 1

            # check for index
            if index in original_line_break_indices:
                encoded_text_with_line_breaks.append('\n\n')

        return encoded_text_with_line_breaks

