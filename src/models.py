import pathlib
import tomllib
from dataclasses import dataclass

import client

path = pathlib.Path('models.toml')
with path.open(mode='rb') as fp:
    MODELS_ZOO = tomllib.load(fp)

@dataclass(unsafe_hash=True)
class RpcLanguageModel:
    name: str
    url: str

    def complete(self, 
        prompt:             str='<|endoftext|>',
        suffix:             str='',
        max_tokens:         int=7, 
        temperature:        float=1.,
        top_p:              float=1.,
        n:                  int=1,
        stream:             bool=False,
        logprobs:           int=0,
        echo:               bool=False,
        stop:               str|list='',
        presence_penalty:   float=0.,
        frequence_penalty:  float=0.,
        best_of:            int=0,
        logit_bias:         dict={},
    ) -> str:
        return client.run(
            url=self.url,
            prompt=prompt, suffix=suffix, max_tokens=max_tokens, temperature=temperature,
            top_p=top_p, n=n, stream=stream, logprobs=logprobs, echo=echo, stop=stop, 
            presence_penalty=presence_penalty, frequence_penalty=frequence_penalty, 
            best_of=best_of, logit_bias=logit_bias
        )
    
    
def get_model(model_id: str, metadata: dict=MODELS_ZOO):
    if model_id in metadata.keys():
        model_url = metadata.get(model_id).get('network', dict()).get('url', None)
        return RpcLanguageModel(name=model_id, url=model_url)
    else:
        return None
    
def list_models(metadata: dict=MODELS_ZOO)-> list:
    return [{'id': key, **meta.get('metadata')} for key, meta in metadata.items()]

def get_model_infos(model_id, metadata: dict=MODELS_ZOO)-> list:
    if model_id in metadata.keys():
        return {'id': model_id, **metadata.get(model_id).get('metadata')}
    return {}
