# openai-code-review-agent
Using OpenAI API to create iterative code review agent

## Usage
To enable this, user needs to purchase API token credits at: https://platform.openai.com/settings/organization/billing/overview.  Out of the available models (as of 06/11/2025) gpt-4o-mini seemed to be the most cost-effective, yet sufficiently performant.  For purposes of code review, a temperature of .2 seemed a good starting point.  See example CLI command below.

### CLI Command
python ../testing/ai/openai-code-review-agent.py path/to/root --model gpt-4o-mini --temperature .2 --ext .tf