import random

from lhotse import CutSet


class ReverbWithImpulseResponse:
    """
    A transform on batch of cuts (``CutSet``) that convolves each cut with an impulse
    response with some probability :attr:`p`. The impulse response is chosen randomly from
    a specified CutSet of RIRs :attr:`rir_cuts`.
    """

    def __init__(
        self,
        rir_cuts: CutSet,
        p: float,
        shift_output: bool = True,
        normalize_output: bool = True,
        randgen: random.Random = None,
        preserve_id: bool = False,
    ) -> None:
        self.rir_cuts = rir_cuts
        self.p = p
        self.shift_output = shift_output
        self.normalize_output = normalize_output
        self.random = randgen
        self.preserve_id = preserve_id

    def __call__(self, cuts: CutSet) -> CutSet:
        if self.random is None:
            self.random = random
        return CutSet.from_cuts(
            cut.reverb_rir(
                rir_cut=self.rir_cuts.sample(n_cuts=1),
                shift_output=self.shift_output,
                normalize_output=self.normalize_output,
                affix_id=not self.preserve_id,
            )
            if self.random.random() >= self.p
            else cut
            for cut in cuts
        )
