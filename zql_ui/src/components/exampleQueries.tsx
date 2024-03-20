export type exampleQuery = {
  title: string;
  query: string;
};

export const exampleQueries: exampleQuery[] = [
  {
    title: "its giving",
    query: "its giving 1\nno cap",
  },
  {
    title: "yass",
    query: "its giving\n\tname,\n\tfave_color\nyass peeps\nno cap",
  },
  {
    title: "sheeeeeesh",
    query: "its giving\n\tsheeeeeesh\nyass peeps\nno cap",
  },
  {
    title: "say less",
    query: "its giving\n\tsheeeeeesh\nyass peeps\nsay less 3\nno cap",
  },
  {
    title: "tfw",
    query: "its giving\n\tsheeeeeesh\nyass peeps\ntfw name be 'vinesh'\nno cap",
  },
  {
    title: "fax",
    query: `its giving
  sheeeeeesh
yass peeps
tfw
  fave_color be 'blue'
  fax followers be 1400
no cap`,
  },
  {
    title: "perchance",
    query: `perchance blue_locked be (
  its giving
    sheeeesh
  yass peeps
  tfw fave_color be 'blue'
)
its giving
  name, dank
yass blue_locked`,
  },
];
